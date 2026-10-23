import tempfile
import unittest
from pathlib import Path

import db


class SchedulingTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.previous_path = db.DB_PATH
        db.DB_PATH = str(Path(self.directory.name) / 'test.db')
        db.init_db()

    def tearDown(self):
        db.DB_PATH = self.previous_path
        self.directory.cleanup()

    def test_initial_slots(self):
        self.assertEqual(db.horarios_disponiveis('2026-11-01'), [f'{h:02d}:00' for h in range(8, 18)])

    def test_booking_removes_slot(self):
        self.assertTrue(db.agendar('Tutor fictício', 'Pet teste', '2026-11-01', '09:00')[0])
        self.assertNotIn('09:00', db.horarios_disponiveis('2026-11-01'))

    def test_duplicate_slot_is_rejected_without_overwriting(self):
        self.assertTrue(db.agendar('Primeiro', 'Pet A', '2026-11-01', '10:00')[0])
        self.assertFalse(db.agendar('Segundo', 'Pet B', '2026-11-01', '10:00')[0])
        with db.get_conn() as conn:
            rows = conn.execute('SELECT tutor FROM agendamentos').fetchall()
        self.assertEqual(rows, [('Primeiro',)])

    def test_same_time_on_another_date_is_available(self):
        db.agendar('Tutor', 'Pet', '2026-11-01', '10:00')
        self.assertIn('10:00', db.horarios_disponiveis('2026-11-02'))

    def test_user_text_is_treated_as_data(self):
        name = "Teste'); DROP TABLE agendamentos; --"
        self.assertTrue(db.agendar(name, 'Pet', '2026-11-01', '11:00')[0])
        with db.get_conn() as conn:
            self.assertEqual(conn.execute('SELECT tutor FROM agendamentos').fetchone()[0], name)

    def test_initialization_is_idempotent(self):
        db.agendar('Tutor', 'Pet', '2026-11-01', '12:00')
        db.init_db()
        self.assertNotIn('12:00', db.horarios_disponiveis('2026-11-01'))


if __name__ == '__main__':
    unittest.main()
