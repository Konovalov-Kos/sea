import functools

class Ship:
    min_ship = 1
    max_ship = 4
    avail_conditions = {
        0: "Живой",
        1: "Ранен",
        2: "Убит",
    }

    def __init__(self, name="", list_coords=None, board_len=10, ):
        self.name = name
        self.board_len = board_len
        self.valid = False
        self.coord_status = dict()
        self.coords = list_coords

    @property
    def mask_ship(self):
        ret = []
        for x, y in self.coords:
            ret += [(x,y), (x + 1, y + 1), (x - 1, y - 1), (x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y), (x + 1, y - 1), (x - 1, y + 1)]
        out = []
        for x,y in ret:
            if x>=0 and y>=0 and x<=self.board_len and y<=self.board_len:
                out.append((x,y))

        return set(  out )

    @property
    def hitted_coords(self):
        ret = set()
        for xy, i in self.coord_status.items():
            if not i:
                ret.add(xy)
        return ret

    @property
    def size(self):
        return len(self.coords)

    @property
    def condition(self):
        try:
            if functools.reduce(lambda x,y: x==y==True, self.coord_status.values()):
                return 0
            if not functools.reduce(lambda x,y: False if x==y==False else True, self.coord_status.values()):
                return 2
            return 1
        except:
            return 4

    def __str__(self):
        return self.name

    @property
    def coords(self):
        if self._coords:
            return self._coords
        else:
            return None

    @coords.setter
    def coords(self, coordlist):
        for x,y in coordlist:
            if x not in range(0,self.board_len) or y not in range(0, self.board_len):
                return
        else:
            cl2 = ((a,b) for a,b in coordlist)
            cl = list(set(cl2))
            if len(cl)!=len(coordlist) or len(cl) > Ship.max_ship or len(cl) < Ship.min_ship:
                print("Неверно!")
                return
            x = set()
            y = set()
            for i,j in coordlist:
                x.add(i)
                y.add(j)
            if len(x)>1 and len(y)>1:
                print("Неверно!")
                return
            rst = list(x) if len(y)==1 else list(y)
            rst.sort()
            if len(rst)-1 == (rst[-1] - rst[0]):
                self._coords = cl
                self.valid = True
                for xy in cl:
                    self.coord_status.update({xy: True})

    def hit(self, xy):
        if xy in self.coords:
            print("Подбита ", xy)
            self.coord_status[xy] = False
            return True
        return False
_rules =  {
    4: 1,
    3: 2,
    2: 3,
    1: 4
}
class Board:
    def __init__(self,uname="playername", size=10, avail_ships=None):
        self.name = uname
        self.ships = []
        self.size = size
        self._cellsize = 30
        self.avail_ship = _rules
        self.all_hit = []

    @property
    def cellsize(self):
        return self._cellsize

    @property
    def get_vid2_json(self):
        '''Вид для оппонеента'''
        ret = { (x,y):0 for x in range(self.size) for y in range(self.size) }
        for xy in self.all_hit:
            ret[xy] = 1
        for ship in self.ships:
            for ship_xy, cond in ship.coord_status.items():
                if not cond:
                    ret[ship_xy] = 2
        return ret

    @property
    def get_vid1_json(self):
        '''Вид для владельца'''
        ret = {(x, y): 0 for x in range(self.size) for y in range(self.size)}
        for xy in self.all_hit:
            ret[xy] = 1
        for ship in self.ships:
            for ship_xy, cond in ship.coord_status.items():
                if not cond:
                    ret[ship_xy] = 2
                else:
                    ret[ship_xy] = 3
        return ret

    @property
    def avail_to_shot(self):
        all_cells = set( (a,b) for a in range(self.size) for b in range(self.size) )
        return all_cells - set(self.all_hit)


    def add(self, sh):
        '''Добавление корабля'''
        if sh.valid:
            for s0 in self.ships:
                for elem in sh.coords:
                    if elem in s0.mask_ship:
                        return False
                # if (sh.mask_ship & s0.mask_ship) != set(): # !!!!!!!!!
                #     return False
            # проверка палубности
            kvo = 0
            for s in self.ships:
                if s.size == sh.size:
                    kvo += 1

            if self.avail_ship[sh.size] > kvo:
                self.ships.append(sh)
                return True
            else:
                print("Не добавляем!!")
        return False

    @property
    def can_start_game(self):
        '''Проверка что расставлены ВСЕ корабли'''
        for palubi, kvo in self.avail_ship.items():
            p = 0
            for s in self.ships:
                if s.size == palubi:
                    p += 1

            if p != kvo:
                return False

        return True

    @property
    def alldead(self):
        '''Все корабли потоплены'''
        # todo: дописать возврат тру фалс
        for elem in self.ships:
            if elem.condition != 2:
                return False
        return True


    def hit(self, target_xy):
        if target_xy[0]>=0 and target_xy[1]>=0 and target_xy[0]<=self.size-1 and target_xy[1]<=self.size-1:
            self.all_hit.append(target_xy)
            for s in self.ships:
                ok = s.hit(target_xy)
                if s.condition == 2:
                    self.all_hit += list(s.mask_ship)
                if ok:
                    return ok
        return False
