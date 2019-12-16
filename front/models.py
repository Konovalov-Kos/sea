from django.contrib.auth.models import User
from django.db import models
import json
import hashlib
from sea.settings import BOARD_SIZE
from .game_obj import Board as GB, Ship
from sea.settings import SECRET_KEY
# Create your models here.

class Board(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ready_to_play = models.BooleanField(default=False)
    ships_data = models.TextField(default='{"ships": [], "hitcoords": []}')

    @property
    def socket_room(self):
        return hashlib.md5(f"{self.id}!{self.user_id}_{SECRET_KEY}".encode("utf-8")).hexdigest()

    @property
    def ships(self):
        try:
            d1 = json.loads(self.ships_data)
            if d1.get('ships') and type(d1.get('ships')) is str:
                d1['ships'] = json.loads(d1['ships'])
            if d1.get('hitcoords') and type(d1.get('hitcoords')) is str:
                d1['hitcoords'] = json.loads(d1['hitcoords'])
            return d1
        except:
            return {}

    @ships.setter
    def ships(self, val):
        try:
            self.ships_data = json.dumps(val)
        except:
            self.ships_data = '{"ships": [], "hitcoords": []}'

    @property
    def brd(self):
        '''На основании сохраненного массива кораблей на доске строим модель доски.'''
        brd = GB(self.user.username)
        try:
            d = self.ships
            # расставить корабли по местам
            for shcoord in d.get("ships", []):
                ship = Ship("some name", shcoord, BOARD_SIZE)
                if ship.valid:
                    brd.add(ship)

            '''Если вдруг состояние готовности к игре не установлено то установить и записать.'''
            if brd.can_start_game and self.ready_to_play == False:
                self.ready_to_play = True
                self.save()

            '''Сейчас все корабли здоровы и веселы. Теперь будем постреливать.'''
            for hitxy in d.get("hitcoords", []):
                brd.hit(hitxy)

        except:
            pass
        return brd

    def hit(self,target_xy):
        try:
            '''логично добавить проверку что стрелять можно когда обе доски расставлены'''

            '''разернули из строки в обьект'''
            d = self.ships
            '''если нет еще выстрелов создали пустой лист'''
            if not d.get('hitcoords'):
                d['hitcoords'] = []
            '''добавили координату куда пострельнули'''
            d['hitcoords'].append(target_xy)
            ret = self.brd.hit(target_xy)
            '''сохранили новое состояние'''
            self.ships = d
            self.save()
            return ret
        except:
            pass


    @property
    def player_view(self):
        '''Возвращает вид для владельца доски. Он видит корабли и покоцанные и целые и выстрелы мимо'''
        return self.brd.get_vid1_json

    @property
    def opponent_view(self):
        return self.brd.get_vid2_json



class Games(models.Model):
    start_time = models.DateTimeField(auto_created=True, auto_now_add=True)
    board1 = models.OneToOneField(Board, on_delete=models.CASCADE, related_name="board1")
    board2 = models.OneToOneField(Board, on_delete=models.CASCADE, blank=True, null=True, related_name="board2")
    firstbturns = models.BooleanField(default=True)
    done = models.BooleanField(default=False)
    winner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

class Menu(models.Model):
    name = models.CharField(max_length=255, blank=False)
    link = models.CharField(max_length=255, blank=False)
    parent = models.ForeignKey('Menu', on_delete=models.CASCADE, null=True, blank=True)
    ochered = models.IntegerField(default=0, blank=True)

    @property
    def has_child(self):
        return Menu.objects.filter(parent=self).exists()

    @property
    def on_site(self):
        ret = '<li class="has_sub">' if self.has_child else '<li>'
        ret += f'''<a href="{self.link}" class="active">{self.name}</a>'''
        if Menu.objects.filter(parent=self).exists():
            ret += '<div class="submenu"><ul>'
            for m in Menu.objects.filter(parent=self).order_by('ochered'):
                ret += m.on_site
            ret += '</ul></div>'
        ret += '</li>'