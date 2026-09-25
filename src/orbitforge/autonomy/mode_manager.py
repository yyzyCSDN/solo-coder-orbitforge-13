from __future__ import annotations

class ModeManager:
    def __init__(self, initial='safe'):
        self.mode = initial
        self.history = [initial]

    def transition(self, target, guards):
        key = (self.mode, target)
        required = guards.get(key, [])
        failed = [name for name, ok in required if not ok]
        if failed:
            return {'changed': False, 'mode': self.mode, 'failed_guards': failed}
        if target != self.mode:
            self.mode = target
            self.history.append(target)
        return {'changed': True, 'mode': self.mode, 'failed_guards': []}

    def rollback(self):
        if len(self.history) < 2:
            return self.mode
        self.history.pop()
        self.mode = self.history[-1]
        return self.mode

    def visit_count(self, mode):
        return sum(1 for x in self.history if x == mode)
