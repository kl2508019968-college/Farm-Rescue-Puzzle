# rules.py
class Rules:
    def __init__(self):
        pass

    def check_lose(self, entities):
        # Hanya semak watak yang ditinggalkan di ATAS DARAT (bukan di dalam bot)
        left = [e.name_en for e in entities if e.side == "left" and not e.on_boat]
        right = [e.name_en for e in entities if e.side == "right" and not e.on_boat]

        def unsafe(side_list):
            # Jika petani ada bersama di atas tebing darat itu, segalanya selamat
            if "Farmer" in side_list:
                return False, ""
                
            # Logik padanan rantai pemakanan baru:
            if "Chicken" in side_list and "Corn" in side_list:
                return True, "CHICKEN_CORN"
            if "Wolf" in side_list and "Chicken" in side_list:
                return True, "WOLF_CHICKEN"
                
            # Lembu + Jagung kini dikira SELAMAT, jadi tiada semakan kalah untuk mereka!
            return False, ""

        # Semak tebing kiri
        lost, code = unsafe(left)
        if lost: return True, code
        
        # Semak tebing kanan
        lost, code = unsafe(right)
        if lost: return True, code

        return False, ""

    def check_win(self, entities):
        # Kemenangan sah apabila semua watak berada di tebing kanan DAN diturunkan sepenuhnya dari bot
        return all(e.side == "right" and not e.on_boat for e in entities)
