import random
import math

class NPCManager:
    def __init__(self, npc_list=None):
        self.npcs = npc_list if npc_list else []

    def add_npc(self, npc):
        self.npcs.append(npc)

    def update_all(self, dt, player):
        for npc in self.npcs:
            self._move_npc(npc, dt)

        for i in range(len(self.npcs)):
            for j in range(i + 1, len(self.npcs)):
                self._handle_collision(self.npcs[i], self.npcs[j])

        for npc in self.npcs:
            self._handle_collision(npc, player)

    def _move_npc(self, npc, dt):
        npc.vx += (random.random() - 0.5) * 0.1
        npc.vy += (random.random() - 0.5) * 0.1

        speed = math.sqrt(npc.vx**2 + npc.vy**2)
        max_speed = getattr(npc, "max_speed", 100)
        if speed > max_speed:
            scale = max_speed / speed
            npc.vx *= scale
            npc.vy *= scale

        npc.x += npc.vx * dt
        npc.y += npc.vy * dt

    def _handle_collision(self, a, b):
        dx = b.x - a.x
        dy = b.y - a.y
        dist_sq = dx * dx + dy * dy
        rsum = getattr(a, "radius", 10) + getattr(b, "radius", 10)
        if dist_sq < rsum * rsum:
            dist = math.sqrt(dist_sq) if dist_sq > 0 else 0.1
            overlap = (rsum - dist) / 2

            nx = dx / dist
            ny = dy / dist

            a.x -= nx * overlap
            a.y -= ny * overlap
            b.x += nx * overlap
            b.y += ny * overlap

            rand_kick = 0.5
            a.vx += (random.random() - 0.5) * rand_kick
            a.vy += (random.random() - 0.5) * rand_kick
            b.vx += (random.random() - 0.5) * rand_kick
            b.vy += (random.random() - 0.5) * rand_kick

            if hasattr(b, "is_player") and b.is_player:
                a.vx *= 0.8
                a.vy *= 0.8
