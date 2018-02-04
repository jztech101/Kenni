#!/usr/bin/env python2
"""
Copyright 2010 Tamas Marki. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice, this list of
      conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright notice, this list
      of conditions and the following disclaimer in the documentation and/or other materials
      provided with the distribution.

THIS SOFTWARE IS PROVIDED BY TAMAS MARKI ``AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL TAMAS MARKI OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


[18:03] <Lako> .play w 3
[18:03] <unobot> TopMobil's turn. Top Card: [*]
[18:03] [Notice] -unobot- Your cards: [4][9][4][8][D2][D2]
[18:03] [Notice] -unobot- Next: hatcher (5 cards) - Lako (2 cards)
[18:03] <TopMobil> :O
[18:03] <Lako> :O

More info:
* Kenni: https://github.com/JZTech101/Kenni
* jenni: https://github.com/myano/jenni/
"""

import random
from datetime import datetime, timedelta
import time

away_last = 0

# Remember to change these 3 lines or nothing will work
CHANNEL = '#techcavern'
SCOREFILE = "~/Kenni/config/unoscores.txt"
# Only the owner (starter of the game) can call .unostop to stop the game.
# But this calls for a way to allow others to stop it after the game has been idle for a while.
# After this set time, anyone can stop the game via .unostop
# Set the time ___in minutes___ here: (default is 5 mins)
INACTIVE_TIMEOUT = 3

STRINGS = {
    'ALREADY_STARTED': '\x0300,01Game already started by %s! Type ".join" to join!',
    'GAME_STARTED': '\x0300,01IRC-UNO started by %s - Type ".join" to join!',
    'GAME_STOPPED': '\x0300,01Game stopped.',
    'CANT_STOP': '\x0300,01%s is the game owner, you can\'t stop it! To force stop the game, please wait %s seconds.',
    'DEALING_IN': '\x0300,01Dealing %s into the game as player #%s!',
    'JOINED': '\x0300,01Dealing %s into the game as player #%s!',
    'ALREADY_JOINED': '\x0300,01Player, %s, is already in the game as player #%s!',
    'ENOUGH': '\x0300,01There are enough players, type .deal to start!',
    'NOT_STARTED': '\x0300,01Game not started, type .uno to start!',
    'NOT_ENOUGH': '\x0300,01Not enough players to deal yet.',
    'NEEDS_TO_DEAL': '\x0300,01%s needs to deal.',
    'ALREADY_DEALT': '\x0300,01Already dealt.',
    'ON_TURN': '\x0300,01It\'s the turn of %s',
    'DONT_HAVE': '\x0300,01You don\'t have that card, %s',
    'DOESNT_PLAY': '\x0300,01That card does not play, %s',
    'UNO': '\x0300,01UNO! %s has ONE card left!',
    'WIN': '\x0300,01We have a winner! %s!!!! This game took %s',
    'DRAWN_ALREADY': '\x0300,01You\'ve already drawn, either .pass or .play!',
    'DRAWS': '\x0300,01%s draws a card',
    'DRAWN_CARD': '\x0300,01Drawn card: %s',
    'DRAW_FIRST': '\x0300,01%s, you need to draw first!',
    'PASSED': '\x0300,01%s passed!',
    'NO_SCORES': '\x0300,01No scores yet',
    'TOP_CARD': '\x0300,01It\'s the turn of %s | Top Card: %s',
    'YOUR_CARDS': '\x0300,01Your cards: %s',
    'NEXT_START': '\x0300,01Next: ',
    'NEXT_PLAYER': '\x0300,01%s (%s cards)',
    'D2': '\x0300,01%s draws two and is skipped!',
    'CARDS': '\x0300,01Cards: %s',
    'WD4': '\x0300,01%s draws four and is skipped!',
    'SKIPPED': '\x0300,01%s is skipped!',
    'REVERSED': '\x0300,01Order reversed!',
    'GAINS': '\x0300,01%s gains %s points!',
    'SCORE_ROW': '\x0300,01%s: #%s %s (%s points, %s games, %s won, %.2f points per game, %.2f percent wins)',
    'GAME_ALREADY_DEALT': '\x0300,01Game has already been dealt, please wait until game is over or stopped.',
    'PLAYER_COLOR_ENABLED': '\x0300,01Hand card colors \x0309,01enabled\x0300,01! Format: <COLOR>/[<CARD>].  Example: R/[D2] is a red Draw Two. Type \'.uno-help\' for more help.',
    'PLAYER_COLOR_DISABLED': '\x0300,01Hand card colors \x0304,01disabled\x0300,01.',
    'DISABLED_PCE': '\x0300,01Hand card colors is \x0304,01disabled\x0300,01 for %s. To enable, \'.pce-on\'',
    'ENABLED_PCE': '\x0300,01Hand card colors is \x0309,01enabled\x0300,01 for %s. To disable, \'.pce-off\'',
    'PCE_CLEARED': '\x0300,01All players\' hand card color setting is reset by %s.',
    'PLAYER_LEAVES': '\x0300,01Player %s has left the game.',
    'OWNER_CHANGE': '\x0300,01Owner %s has left the game. New owner is %s.',
}

class UnoBot:
    def __init__(self):
        self.colored_card_nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'R', 'S', 'D2']
        self.special_scores = {'R' : 20, 'S' : 20, 'D2' : 20, 'W' : 50, 'WD4' : 50}
        self.colors = 'RGBY'
        self.special_cards = ['W', 'WD4']
        self.players = dict()
        self.owners = dict()
        self.players_pce = dict()  # Player color enabled hash table
        self.playerOrder = list()
        self.game_on = False
        self.currentPlayer = 0
        self.topCard = None
        self.way = 1
        self.drawn = False
        self.scoreFile = SCOREFILE
        self.deck = list()
        self.prescores = list()
        self.dealt = False
        self.lastActive = datetime.now()
        self.timeout = timedelta(minutes=INACTIVE_TIMEOUT)

    def start(self, kenni, owner):
        owner = owner.lower()
        if self.game_on:
            kenni.msg(CHANNEL, STRINGS['ALREADY_STARTED'] % self.game_on)
        else:
            self.lastActive = datetime.now()
            self.game_on = owner
            self.deck = list()
            kenni.msg(CHANNEL, STRINGS['GAME_STARTED'] % owner)
            self.players = dict()
            self.players[owner] = list()
            self.playerOrder = [owner]
            kenni.msg(CHANNEL, STRINGS['JOINED'] % (owner, self.playerOrder.index(owner) + 1))
            if self.players_pce.get(owner, 0):
                kenni.notice(owner, STRINGS['ENABLED_PCE'] % owner)

    def stop(self, kenni, input):
        nickk = (input.nick).lower()
        tmptime = datetime.now()
        if nickk == self.game_on or tmptime - self.lastActive > self.timeout:
            kenni.msg(CHANNEL, STRINGS['GAME_STOPPED'])
            self.game_on = False
            self.dealt = False
        elif self.game_on:
            kenni.msg(CHANNEL, STRINGS['CANT_STOP'] % (self.game_on, self.timeout.seconds - (tmptime - self.lastActive).seconds))

    def join(self, kenni, input):
        #print dir(kenni)
        #print dir(input)
        nickk = (input.nick).lower()
        if self.game_on:
            if not self.dealt:
                if nickk not in self.players:
                    self.players[nickk] = list()
                    self.playerOrder.append(nickk)
                    self.lastActive = datetime.now()
                    if self.players_pce.get(nickk, 0):
                        kenni.notice(nickk, STRINGS['ENABLED_PCE'] % nickk)
                    if self.deck:
                        for i in xrange(0, 7):
                            self.players[nickk].append(self.getCard())
                        kenni.msg(CHANNEL, STRINGS['DEALING_IN'] % (nickk, self.playerOrder.index(nickk) + 1))
                    else:
                        kenni.msg(CHANNEL, STRINGS['JOINED'] % (nickk, self.playerOrder.index(nickk) + 1))
                        if len (self.players) == 2:
                            kenni.msg(CHANNEL, STRINGS['ENOUGH'])
                else:
                    kenni.msg(CHANNEL, STRINGS['ALREADY_JOINED'] % (nickk, self.playerOrder.index(nickk) + 1))
            else:
                kenni.msg(CHANNEL, STRINGS['GAME_ALREADY_DEALT'])
        else:
            kenni.msg(CHANNEL, STRINGS['NOT_STARTED'])

    def deal(self, kenni, input):
        nickk = (input.nick).lower()
        if not self.game_on:
            kenni.msg(CHANNEL, STRINGS['NOT_STARTED'])
            return
        if len(self.players) < 2:
            kenni.msg(CHANNEL, STRINGS['NOT_ENOUGH'])
            return
        if nickk != self.game_on:
            kenni.msg(CHANNEL, STRINGS['NEEDS_TO_DEAL'] % self.game_on)
            return
        if len(self.deck):
            kenni.msg(CHANNEL, STRINGS['ALREADY_DEALT'])
            return
        self.startTime = datetime.now()
        self.lastActive = datetime.now()
        self.deck = self.createnewdeck()
        for i in xrange(0, 7):
            for p in self.players:
                self.players[p].append(self.getCard ())
        self.topCard = self.getCard()
        while self.topCard.lstrip(self.colors) in 'R S D2 W WD4':
           self.topCard = self.getCard()
        self.currentPlayer = 1
        self.cardPlayed(kenni, self.topCard)
        self.showOnTurn(kenni)
        self.dealt = True

    def play(self, kenni, input):
        nickk = (input.nick).lower()
        if not self.game_on or not self.deck:
            return
        if nickk != self.playerOrder[self.currentPlayer]:
            kenni.msg(CHANNEL, STRINGS['ON_TURN'] % self.playerOrder[self.currentPlayer])
            return
        tok = [z.strip() for z in str(input).upper().split(' ')]
        if len(tok) != 3:
            return
        searchcard = str()
        if tok[1] in self.special_cards and tok[2] in self.colors:
            searchcard = tok[1]
        elif tok[1] in self.colors:
            searchcard = (tok[1] + tok[2])
        else:
            kenni.msg(CHANNEL, STRINGS['DOESNT_PLAY'] % self.playerOrder[self.currentPlayer])
            return
        if searchcard not in self.players[self.playerOrder[self.currentPlayer]]:
            kenni.msg(CHANNEL, STRINGS['DONT_HAVE'] % self.playerOrder[self.currentPlayer])
            return
        playcard = (tok[1] + tok[2])
        if not self.cardPlayable(playcard):
            kenni.msg(CHANNEL, STRINGS['DOESNT_PLAY'] % self.playerOrder[self.currentPlayer])
            return

        self.drawn = False
        self.players[self.playerOrder[self.currentPlayer]].remove(searchcard)

        pl = self.currentPlayer

        self.incPlayer()
        self.cardPlayed(kenni, playcard)

        if len(self.players[self.playerOrder[pl]]) == 1:
            kenni.msg(CHANNEL, STRINGS['UNO'] % self.playerOrder[pl])
        elif len(self.players[self.playerOrder[pl]]) == 0:
            kenni.msg(CHANNEL, STRINGS['WIN'] % (self.playerOrder[pl], (datetime.now() - self.startTime)))
            self.gameEnded(kenni, self.playerOrder[pl])
            return

        self.lastActive = datetime.now()
        self.showOnTurn(kenni)

    def draw(self, kenni, input):
        nickk = (input.nick).lower()
        if not self.game_on or not self.deck:
            return
        if nickk != self.playerOrder[self.currentPlayer]:
            kenni.msg(CHANNEL, STRINGS['ON_TURN'] % self.playerOrder[self.currentPlayer])
            return
        if self.drawn:
            kenni.msg(CHANNEL, STRINGS['DRAWN_ALREADY'])
            return
        self.drawn = True
        kenni.msg(CHANNEL, STRINGS['DRAWS'] % self.playerOrder[self.currentPlayer])
        c = self.getCard()
        self.players[self.playerOrder[self.currentPlayer]].append(c)
        self.lastActive = datetime.now()
        kenni.notice(nickk, STRINGS['DRAWN_CARD'] % self.renderCards (nickk, [c], 0))

    # this is not a typo, avoiding collision with Python's pass keyword
    def passs(self, kenni, input):
        nickk = (input.nick).lower()
        if not self.game_on or not self.deck:
            return
        if nickk != self.playerOrder[self.currentPlayer]:
            kenni.msg(CHANNEL, STRINGS['ON_TURN'] % self.playerOrder[self.currentPlayer])
            return
        if not self.drawn:
            kenni.msg(CHANNEL, STRINGS['DRAW_FIRST'] % self.playerOrder[self.currentPlayer])
            return
        self.drawn = False
        kenni.msg(CHANNEL, STRINGS['PASSED'] % self.playerOrder[self.currentPlayer])
        self.incPlayer()
        self.lastActive = datetime.now()
        self.showOnTurn(kenni)

    def top10(self, kenni, input):
        nickk = (input.nick).lower()
        self.rankings("ppg")
        i = 1
        for z in self.prescores[:10]:
            kenni.msg(nickk, STRINGS['SCORE_ROW'] % ('ppg', i, z[0], z[3], z[1], z[2], float(z[3])/float(z[1]), float(z[2])/float(z[1])*100))
            i += 1

    def createnewdeck(self):
        ret = list()

        for i in range(2):
            for a in self.colored_card_nums:
                for b in self.colors:
                    if i > 0 and a == '0':
                        continue
                    ret.append(b + a)
                random.SystemRandom().shuffle(ret)

        for a in self.special_cards:
            for i in range(4):
                ret.append(a)
                random.SystemRandom().shuffle(ret)

        if len(self.playerOrder) > 4:
            ret *= 2

        random.SystemRandom().shuffle(ret)

        return ret

    def getCard(self):
        ret = self.deck[0]
        self.deck.pop(0)
        if not self.deck:
            self.deck = self.createnewdeck()
        return ret

    def showOnTurn(self, kenni):
        kenni.msg(CHANNEL, STRINGS['TOP_CARD'] % (self.playerOrder[self.currentPlayer], self.renderCards(None, [self.topCard], 1)))
        kenni.notice(self.playerOrder[self.currentPlayer], STRINGS['YOUR_CARDS'] % self.renderCards(self.playerOrder[self.currentPlayer], self.players[self.playerOrder[self.currentPlayer]], 0))
        msg = STRINGS['NEXT_START']
        tmp = self.currentPlayer + self.way
        if tmp == len(self.players):
            tmp = 0
        if tmp < 0:
            tmp = len(self.players) - 1
        arr = list()
        while tmp != self.currentPlayer:
            arr.append(STRINGS['NEXT_PLAYER'] % (self.playerOrder[tmp], len(self.players[self.playerOrder[tmp]])))
            tmp = tmp + self.way
            if tmp == len(self.players):
                tmp = 0
            if tmp < 0:
                tmp = len(self.players) - 1
        msg += ' - '.join(arr)
        kenni.notice(self.playerOrder[self.currentPlayer], msg)

    def showCards(self, kenni, user):
        user = user.lower()
        if not self.game_on or not self.deck:
            return
        msg = STRINGS['NEXT_START']
        tmp = self.currentPlayer + self.way
        if tmp == len(self.players):
            tmp = 0
        if tmp < 0:
            tmp = len(self.players) - 1
        arr = list()
        k = len(self.players)
        while k > 0:
            arr.append(STRINGS['NEXT_PLAYER'] % (self.playerOrder[tmp], len(self.players[self.playerOrder[tmp]])))
            tmp = tmp + self.way
            if tmp == len(self.players):
                tmp = 0
            if tmp < 0:
                tmp = len(self.players) - 1
            k-=1
        msg += ' - '.join(arr)
        if user not in self.players:
            kenni.notice(user, msg)
        else:
            kenni.notice(user, STRINGS['YOUR_CARDS'] % self.renderCards(user, self.players[user], 0))
            kenni.notice(user, msg)

    def renderCards(self, nick, cards, is_chan):
        nickk = nick
        if nick:
            nickk = (nick).lower()
        ret = list()
        for c in sorted(cards):
            if c in ['W', 'WD4']:
                sp = str()
                if not is_chan and self.players_pce.get(nickk, 0):
                    sp = ' '
                ret.append('\x0300,01[' + c + ']' + sp)
                continue
            if c[0] == 'W':
                c = c[-1] + '*'
            t = '\x0300,01\x03'
            if c[0] == 'B':
                t += '11,01'
            elif c[0] == 'Y':
                t += '08,01'
            elif c[0] == 'G':
                t += '09,01'
            elif c[0] == 'R':
                t += '04,01'
            if not is_chan:
                if self.players_pce.get(nickk, 0):
                    t += '%s/ [%s]  ' % (c[0], c[1:])
                else:
                    t += '[%s]' % c[1:]
            else:
                t += '(%s) [%s]' % (c[0], c[1:])
            t += "\x0300,01"
            ret.append(t)
        return ''.join(ret)

    def cardPlayable(self, card):
        if card[0] == 'W' and card[-1] in self.colors:
            return True
        if self.topCard[0] == 'W':
            return card[0] == self.topCard[-1]
        return (card[0] == self.topCard[0]) or (card[1] == self.topCard[1])

    def cardPlayed(self, kenni, card):
        if card[1:] == 'D2':
            kenni.msg(CHANNEL, STRINGS['D2'] % self.playerOrder[self.currentPlayer])
            z = [self.getCard(), self.getCard()]
            kenni.notice(self.playerOrder[self.currentPlayer], STRINGS['CARDS'] % self.renderCards(self.playerOrder[self.currentPlayer], z, 0))
            self.players[self.playerOrder[self.currentPlayer]].extend (z)
            self.incPlayer()
        elif card[:2] == 'WD':
            kenni.msg(CHANNEL, STRINGS['WD4'] % self.playerOrder[self.currentPlayer])
            z = [self.getCard(), self.getCard(), self.getCard(), self.getCard()]
            kenni.notice(self.playerOrder[self.currentPlayer], STRINGS['CARDS'] % self.renderCards(self.playerOrder[self.currentPlayer], z, 0))
            self.players[self.playerOrder[self.currentPlayer]].extend(z)
            self.incPlayer()
        elif card[1] == 'S':
            kenni.msg(CHANNEL, STRINGS['SKIPPED'] % self.playerOrder[self.currentPlayer])
            self.incPlayer()
        elif card[1] == 'R' and card[0] != 'W':
            kenni.msg(CHANNEL, STRINGS['REVERSED'])
            if len(self.players) > 2:
                self.way = -self.way
                self.incPlayer()
                self.incPlayer()
            else:
                self.incPlayer()
        self.topCard = card

    def gameEnded(self, kenni, winner):
        try:
            score = 0
            for p in self.players:
                for c in self.players[p]:
                    if c[0] == 'W':
                        score += self.special_scores[c]
                    elif c[1] in [ 'S', 'R', 'D' ]:
                        score += self.special_scores[c[1:]]
                    else:
                        score += int(c[1])
            kenni.msg(CHANNEL, STRINGS['GAINS'] % (winner, score))
            self.saveScores(self.players.keys(), winner, score, (datetime.now() - self.startTime).seconds)
        except Exception, e:
            print 'Score error: %s' % e
        self.players = dict()
        self.playerOrder = list()
        self.game_on = False
        self.currentPlayer = 0
        self.topCard = None
        self.way = 1
        self.dealt = False


    def incPlayer(self):
        self.currentPlayer = self.currentPlayer + self.way
        if self.currentPlayer == len(self.players):
            self.currentPlayer = 0
        if self.currentPlayer < 0:
            self.currentPlayer = len(self.players) - 1

    def saveScores(self, players, winner, score, time):
        from copy import copy
        prescores = dict()
        try:
            f = open(self.scoreFile, 'r')
            for l in f:
                t = l.replace('\n', '').split(' ')
                if len (t) < 4: continue
                if len (t) == 4: t.append(0)
                prescores[t[0]] = [t[0], int(t[1]), int(t[2]), int(t[3]), int(t[4])]
            f.close()
        except: pass
        for p in players:
            p = p.lower()
            if p not in prescores:
                prescores[p] = [ p, 0, 0, 0, 0 ]
            prescores[p][1] += 1
            prescores[p][4] += time
        prescores[winner][2] += 1
        prescores[winner][3] += score
        try:
            f = open(self.scoreFile, 'w')
            for p in prescores:
                f.write(' '.join ([str(s) for s in prescores[p]]) + '\n')
            f.close()
        except Exception, e:
            print 'Failed to write score file %s' % e

    # Custom added functions ============================================== #
    def rankings(self, rank_type):
        from copy import copy
        self.prescores = list()
        try:
            f = open(self.scoreFile, 'r')
            for l in f:
                t = l.replace('\n', '').split(' ')
                if len(t) < 4: continue
                self.prescores.append(copy (t))
                if len(t) == 4: t.append(0)
            f.close()
        except: pass
        if rank_type == "ppg":
            self.prescores = sorted(self.prescores, lambda x, y: cmp((y[1] != '0') and (float(y[3]) / int(y[1])) or 0, (x[1] != '0') and (float(x[3]) / int(x[1])) or 0))
        elif rank_type == "pw":
            self.prescores = sorted(self.prescores, lambda x, y: cmp((y[1] != '0') and (float(y[2]) / int(y[1])) or 0, (x[1] != '0') and (float(x[2]) / int(x[1])) or 0))

    def showTopCard_demand(self, kenni):
        if not self.game_on or not self.deck:
            return
        kenni.say(STRINGS['TOP_CARD'] % (self.playerOrder[self.currentPlayer], self.renderCards(None, [self.topCard], 1)))

    def leave(self, kenni, input):
        nickk = (input.nick).lower()
        self.remove_player(kenni, nickk)

    def remove_player(self, kenni, nick):
        if not self.game_on:
            return

        user = self.players.get(nick, None)
        if user is not None:
            numPlayers = len(self.playerOrder)

            self.playerOrder.remove(nick)
            del self.players[nick]

            if self.way == 1 and self.currentPlayer == numPlayers - 1:
                self.currentPlayer = 0
            elif self.way == -1:
                if self.currentPlayer == 0:
                    self.currentPlayer = numPlayers - 2
                else:
                    self.currentPlayer -= 1

            kenni.msg(CHANNEL, STRINGS['PLAYER_LEAVES'] % nick)
            if numPlayers == 2 and self.dealt or numPlayers == 1:
                kenni.msg(CHANNEL, STRINGS['GAME_STOPPED'])
                self.game_on = None
                self.dealt = None
                return

            if self.game_on == nick:
                self.game_on = self.playerOrder[0]
                kenni.msg(CHANNEL, STRINGS['OWNER_CHANGE'] % (nick, self.playerOrder[0]))

            if self.dealt:
                kenni.msg(CHANNEL, STRINGS['TOP_CARD'] % (self.playerOrder[self.currentPlayer], self.renderCards(None, [self.topCard], 1)))

    def enablePCE(self, kenni, nick):
        nickk = nick.lower()
        if not self.players_pce.get(nickk, 0):
            self.players_pce.update({ nickk : 1})
            kenni.notice(nickk, STRINGS['PLAYER_COLOR_ENABLED'])
        else:
            kenni.notice(nickk, STRINGS['ENABLED_PCE'] % nickk)

    def disablePCE(self, kenni, nick):
        nickk = nick.lower()
        if self.players_pce.get(nickk, 0):
            self.players_pce.update({ nickk : 0})
            kenni.notice(nickk, STRINGS['PLAYER_COLOR_DISABLED'])
        else:
            kenni.notice(nickk, STRINGS['DISABLED_PCE'] % nickk)

    def isPCEEnabled(self, kenni, nick):
        nickk = nick.lower()
        if not self.players_pce.get(nickk, 0):
            kenni.notice(nickk, STRINGS['DISABLED_PCE'] % nickk)
        else:
            kenni.notice(nickk, STRINGS['ENABLED_PCE'] % nickk)

    def PCEClear(self, kenni, nick):
        nickk = nick.lower()
        if not self.owners.get(nickk, 0):
            self.players_pce.clear()
            kenni.msg(CHANNEL, STRINGS['PCE_CLEARED'] % nickk)

    def unostat(self, kenni, input):
        text = input.group().lower().split()

        if len(text) != 3:
            kenni.reply("Invalid input for stats command. Try '.unostats ppg 10' to show the top 10 ranked by points per game. You can also show rankings by percent-wins 'pw'.")
            return

        if text[1] == "pw" or text[1] == "ppg":
            self.rankings(text[1])
            self.rank_assist(kenni, input, text[2], text[1])

        if not self.prescores:
            kenni.reply(STRINGS['NO_SCORES'])

    def rank_assist(self, kenni, input, nicknum, ranktype):
        nickk = (input.nick).lower()
        if nicknum.isdigit():
            i = 1
            s = int(nicknum)
            for z in self.prescores[:s]:
                kenni.msg(nickk, STRINGS['SCORE_ROW'] % (ranktype, i, z[0], z[3], z[1], z[2], float(z[3])/float(z[1]), float(z[2])/float(z[1])*100))
                i += 1
        else:
            j = 1
            t = str(nicknum)
            for y in self.prescores:
                if y[0] == t:
                    kenni.say(STRINGS['SCORE_ROW'] % (ranktype, j, y[0], y[3], y[1], y[2], float(y[3])/float(y[1]), float(y[2])/float(y[1])*100))
                j += 1

unobot = UnoBot ()

def uno(kenni, input):
    if input.sender != CHANNEL:
        kenni.reply("Please join %s to play uno!" % (CHANNEL))
    elif input.sender == CHANNEL:
        unobot.start(kenni, input.nick)
uno.commands = ['uno']
uno.priority = 'low'
uno.thread = False
uno.rate = 0

def unostop(kenni, input):
    if not (input.sender).startswith('#'):
        return
    unobot.stop(kenni, input)
unostop.commands = ['unostop']
unostop.priority = 'low'
unostop.thread = False
unostop.rate = 0

def unojoin(kenni, input):
    if not (input.sender).startswith('#'):
        return
    if input.sender == CHANNEL:
        unobot.join(kenni, input)
unojoin.commands = ['ujoin', 'join']
unojoin.priority = 'low'
unojoin.thread = False
unojoin.rate = 0

def deal(kenni, input):
    if not (input.sender).startswith('#'):
        return
    unobot.deal(kenni, input)
deal.commands = ['deal']
deal.priority = 'low'
deal.thread = False
deal.rate = 0

def play(kenni, input):
    if not (input.sender).startswith('#'):
        return
    unobot.play(kenni, input)
play.commands = ['play', 'p']
play.priority = 'low'
play.thread = False
play.rate = 0

def draw(kenni, input):
    if not (input.sender).startswith('#'):
        return
    unobot.draw(kenni, input)
draw.commands = ['draw', 'd', 'dr']
draw.priority = 'low'
draw.thread = False
draw.rate = 0

def passs(kenni, input):
    if not (input.sender).startswith('#'):
        return
    unobot.passs(kenni, input)
passs.commands = ['pass', 'pa']
passs.priority = 'low'
passs.thread = False
passs.rate = 0

def unotop10(kenni, input):
    unobot.top10(kenni, input)
unotop10.commands = ['unotop10']
unotop10.priority = 'low'
unotop10.thread = False
unotop10.rate = 0

def show_user_cards(kenni, input):
    unobot.showCards(kenni, input.nick)
show_user_cards.commands = ['cards']
show_user_cards.priority = 'low'
show_user_cards.thread = False
show_user_cards.rate = 0

def top_card(kenni, input):
    if not (input.sender).startswith('#'):
        return
    unobot.showTopCard_demand(kenni)
top_card.commands = ['top']
top_card.priority = 'low'
top_card.thread = False
top_card.rate = 0

def leave(kenni, input):
    if not (input.sender).startswith('#'):
        return
    unobot.leave(kenni, input)
leave.commands = ['leave']
leave.priority = 'low'
leave.thread = False
leave.rate = 0

def remove_on_part(kenni, input):
    if input.sender == CHANNEL:
        unobot.remove_player(kenni, (input.nick).lower())
remove_on_part.event = 'PART'
remove_on_part.rule = '.*'
remove_on_part.priority = 'low'
remove_on_part.thread = False
remove_on_part.rate = 0

def remove_on_quit(kenni, input):
    if input.sender == CHANNEL:
        unobot.remove_player(kenni, (input.nick).lower())
remove_on_quit.event = 'QUIT'
remove_on_quit.rule = '.*'
remove_on_quit.priority = 'low'
remove_on_quit.thread = False
remove_on_quit.rate = 0

def remove_on_kick(kenni, input):
    if input.sender == CHANNEL:
        unobot.remove_player(kenni, (input.args[1].lower()))
remove_on_kick.event = 'KICK'
remove_on_kick.rule = '.*'
remove_on_kick.priority = 'low'
remove_on_kick.thread = False
remove_on_kick.rate = 0

def remove_on_nickchg(kenni, input):
    unobot.remove_player(kenni, (input.nick).lower())
remove_on_nickchg.event = 'NICK'
remove_on_nickchg.rule = '.*'
remove_on_nickchg.priority = 'low'
remove_on_nickchg.thread = False
remove_on_nickchg.rate = 0

def unostats(kenni, input):
    unobot.unostat(kenni, input)
unostats.commands = ['unostats']
unostats.priority = 'low'
unostats.thread = False
unostats.rate = 0

def uno_help(kenni, input):
    nick = input.group(2)
    txt = 'For rules, examples, and getting started: https://is.gd/4YxydS'
    if nick:
        nick = (nick).strip()
        output = "%s, %s" % (nick, txt)
    else:
        output = txt
    kenni.say(output)
uno_help.commands = ['uno-help', 'unohelp']
uno_help.priority = 'low'
uno_help.thread = False
uno_help.rate = 0

def uno_pce_on(kenni, input):
    unobot.enablePCE(kenni, input.nick)
uno_pce_on.commands = ['pce-on']
uno_pce_on.priority = 'low'
uno_pce_on.thread = False
uno_pce_on.rate = 0

def uno_pce_off(kenni, input):
    unobot.disablePCE(kenni, input.nick)
uno_pce_off.commands = ['pce-off']
uno_pce_off.priority = 'low'
uno_pce_off.thread = False
uno_pce_off.rate = 0

def uno_ispce(kenni, input):
    unobot.isPCEEnabled(kenni, input.nick)
uno_ispce.commands = ['pce']
uno_ispce.priority = 'low'
uno_ispce.thread = False
uno_ispce.rate = 0

def uno_pce_clear(kenni, input):
    unobot.PCEClear(kenni, input.nick)
uno_pce_clear.commands = ['.pce-clear']
uno_pce_clear.priority = 'low'
uno_pce_clear.thread = False
uno_pce_clear.rate = 0

user_triggered = False

if __name__ == '__main__':
    print __doc__.strip()
