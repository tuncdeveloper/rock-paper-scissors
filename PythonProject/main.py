#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Taş Kağıt Makas Oyunu
Modern ve animasyonlu masaüstü oyunu

Kullanım: python main.py
"""

import tkinter as tk
import random
from enum import Enum
import threading


# Game Service (Oyun Mantığı)
class Choice(Enum):
    ROCK = "taş"
    PAPER = "kağıt"
    SCISSORS = "makas"


class GameResult(Enum):
    WIN = "kazandın"
    LOSE = "kaybettin"
    DRAW = "berabere"


class GameService:
    """Oyun mantığını yöneten servis sınıfı"""

    def __init__(self):
        self.player_score = 0
        self.computer_score = 0
        self.total_games = 0

        # Oyun kuralları
        self.rules = {
            Choice.ROCK: Choice.SCISSORS,
            Choice.PAPER: Choice.ROCK,
            Choice.SCISSORS: Choice.PAPER
        }

        # Emoji mappings
        self.choice_emojis = {
            Choice.ROCK: "🗿",
            Choice.PAPER: "📄",
            Choice.SCISSORS: "✂️"
        }

    def get_computer_choice(self):
        """Bilgisayarın rastgele seçim yapması"""
        return random.choice(list(Choice))

    def determine_winner(self, player_choice, computer_choice):
        """Kazananı belirle"""
        if player_choice == computer_choice:
            return GameResult.DRAW
        elif self.rules[player_choice] == computer_choice:
            return GameResult.WIN
        else:
            return GameResult.LOSE

    def play_round(self, player_choice):
        """Bir tur oyna ve sonucu döndür"""
        computer_choice = self.get_computer_choice()
        result = self.determine_winner(player_choice, computer_choice)

        # Skoru güncelle
        self.total_games += 1
        if result == GameResult.WIN:
            self.player_score += 1
        elif result == GameResult.LOSE:
            self.computer_score += 1

        return computer_choice, result

    def get_score(self):
        """Mevcut skoru döndür (oyuncu, bilgisayar)"""
        return self.player_score, self.computer_score

    def get_choice_emoji(self, choice):
        """Seçim için emoji döndür"""
        return self.choice_emojis[choice]

    def reset_game(self):
        """Oyunu sıfırla"""
        self.player_score = 0
        self.computer_score = 0
        self.total_games = 0

    def get_win_percentage(self):
        """Kazanma yüzdesini hesapla"""
        if self.total_games == 0:
            return 0.0
        return (self.player_score / self.total_games) * 100


# Game UI (Arayüz)
class GameUI:
    """Modern arayüz sınıfı"""

    def __init__(self, root):
        self.root = root
        self.game_service = GameService()
        self.animation_running = False
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        """Pencere ayarları"""
        self.root.title("🎮 Taş Kağıt Makas Oyunu")

        # Ekran boyutunu al
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Pencere boyutunu ekran boyutuna göre ayarla
        window_width = min(1000, int(screen_width * 0.8))
        window_height = min(700, int(screen_height * 0.8))

        self.root.geometry(f"{window_width}x{window_height}")
        self.root.configure(bg='#1a1a2e')
        self.root.resizable(True, True)  # Yeniden boyutlandırılabilir yap
        self.root.minsize(800, 600)  # Minimum boyut

        # Pencereyi ortala
        self.root.update_idletasks()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def create_widgets(self):
        """Widget'ları oluştur"""
        # Ana frame - scrollable frame ekle
        canvas = tk.Canvas(self.root, bg='#1a1a2e', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1a1a2e')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Ana frame
        main_frame = tk.Frame(scrollable_frame, bg='#1a1a2e')
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)

        # Başlık
        title_label = tk.Label(main_frame,
                               text="🎮 TAŞ KAĞIT MAKAS",
                               font=('Arial', 28, 'bold'),
                               fg='#4fc3f7',
                               bg='#1a1a2e')
        title_label.pack(pady=(0, 15))

        # Skor paneli
        self.create_score_panel(main_frame)

        # Oyun alanı
        game_frame = tk.Frame(main_frame, bg='#1a1a2e')
        game_frame.pack(fill='both', expand=True, pady=15)

        # Oyuncu ve bilgisayar seçim alanları
        choices_frame = tk.Frame(game_frame, bg='#1a1a2e')
        choices_frame.pack(fill='both', expand=True, pady=15)

        # Oyuncu alanı
        player_frame = tk.Frame(choices_frame, bg='#16213e', relief='raised', bd=2)
        player_frame.pack(side='left', fill='both', expand=True, padx=(0, 8))

        tk.Label(player_frame, text="SEN", font=('Arial', 18, 'bold'),
                 fg='#4fc3f7', bg='#16213e').pack(pady=10)

        self.player_choice_label = tk.Label(player_frame, text="❓",
                                            font=('Arial', 80),
                                            bg='#16213e', fg='white')
        self.player_choice_label.pack(pady=25)

        # VS etiketi
        vs_label = tk.Label(choices_frame, text="VS",
                            font=('Arial', 24, 'bold'),
                            fg='#ff6b6b', bg='#1a1a2e')
        vs_label.pack(side='left', padx=15)

        # Bilgisayar alanı
        computer_frame = tk.Frame(choices_frame, bg='#16213e', relief='raised', bd=2)
        computer_frame.pack(side='right', fill='both', expand=True, padx=(8, 0))

        tk.Label(computer_frame, text="BİLGİSAYAR", font=('Arial', 18, 'bold'),
                 fg='#ff6b6b', bg='#16213e').pack(pady=10)

        self.computer_choice_label = tk.Label(computer_frame, text="❓",
                                              font=('Arial', 80),
                                              bg='#16213e', fg='white')
        self.computer_choice_label.pack(pady=25)

        # Sonuç etiketi
        self.result_label = tk.Label(game_frame, text="Seçimini yap!",
                                     font=('Arial', 20, 'bold'),
                                     fg='#4fc3f7', bg='#1a1a2e')
        self.result_label.pack(pady=20)

        # Butonlar
        self.create_buttons(main_frame)

        # Canvas ve scrollbar'ı pack et
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_score_panel(self, parent):
        """Skor paneli oluştur"""
        score_frame = tk.Frame(parent, bg='#16213e', relief='raised', bd=2)
        score_frame.pack(fill='x', pady=(0, 10))

        # Oyuncu skoru
        player_score_frame = tk.Frame(score_frame, bg='#16213e')
        player_score_frame.pack(side='left', fill='both', expand=True)

        tk.Label(player_score_frame, text="SENİN SKORUN",
                 font=('Arial', 12, 'bold'), fg='#4fc3f7', bg='#16213e').pack(pady=5)
        self.player_score_label = tk.Label(player_score_frame, text="0",
                                           font=('Arial', 20, 'bold'),
                                           fg='white', bg='#16213e')
        self.player_score_label.pack()

        # Ayırıcı
        separator = tk.Frame(score_frame, width=2, bg='#4fc3f7')
        separator.pack(side='left', fill='y', padx=20)

        # İstatistikler
        stats_frame = tk.Frame(score_frame, bg='#16213e')
        stats_frame.pack(side='left', fill='both', expand=True)

        tk.Label(stats_frame, text="KAZANMA ORANI",
                 font=('Arial', 12, 'bold'), fg='#4fc3f7', bg='#16213e').pack(pady=5)
        self.win_rate_label = tk.Label(stats_frame, text="0%",
                                       font=('Arial', 20, 'bold'),
                                       fg='white', bg='#16213e')
        self.win_rate_label.pack()

        # Ayırıcı
        separator2 = tk.Frame(score_frame, width=2, bg='#4fc3f7')
        separator2.pack(side='left', fill='y', padx=20)

        # Bilgisayar skoru
        computer_score_frame = tk.Frame(score_frame, bg='#16213e')
        computer_score_frame.pack(side='right', fill='both', expand=True)

        tk.Label(computer_score_frame, text="BİLGİSAYAR SKORU",
                 font=('Arial', 12, 'bold'), fg='#ff6b6b', bg='#16213e').pack(pady=5)
        self.computer_score_label = tk.Label(computer_score_frame, text="0",
                                             font=('Arial', 20, 'bold'),
                                             fg='white', bg='#16213e')
        self.computer_score_label.pack()

    def create_buttons(self, parent):
        """Oyun butonları oluştur"""
        button_frame = tk.Frame(parent, bg='#1a1a2e')
        button_frame.pack(pady=20, fill='x')

        # Seçim butonları
        choices_button_frame = tk.Frame(button_frame, bg='#1a1a2e')
        choices_button_frame.pack(pady=(0, 15))

        # Buton boyutlarını artır
        button_width = 10
        button_height = 4

        self.rock_btn = tk.Button(choices_button_frame, text="🗿\nTAŞ",
                                  font=('Arial', 16, 'bold'),
                                  bg='#16213e', fg='white',
                                  activebackground='#0f3460',
                                  width=button_width, height=button_height,
                                  command=lambda: self.play_choice(Choice.ROCK))
        self.rock_btn.pack(side='left', padx=15)

        self.paper_btn = tk.Button(choices_button_frame, text="📄\nKAĞIT",
                                   font=('Arial', 16, 'bold'),
                                   bg='#16213e', fg='white',
                                   activebackground='#0f3460',
                                   width=button_width, height=button_height,
                                   command=lambda: self.play_choice(Choice.PAPER))
        self.paper_btn.pack(side='left', padx=15)

        self.scissors_btn = tk.Button(choices_button_frame, text="✂️\nMAKAS",
                                      font=('Arial', 16, 'bold'),
                                      bg='#16213e', fg='white',
                                      activebackground='#0f3460',
                                      width=button_width, height=button_height,
                                      command=lambda: self.play_choice(Choice.SCISSORS))
        self.scissors_btn.pack(side='left', padx=15)

        # Kontrol butonları
        control_frame = tk.Frame(button_frame, bg='#1a1a2e')
        control_frame.pack()

        reset_btn = tk.Button(control_frame, text="🔄 YENİDEN BAŞLA",
                              font=('Arial', 14, 'bold'),
                              bg='#ff6b6b', fg='white',
                              activebackground='#ff5252',
                              padx=20, pady=10,
                              command=self.reset_game)
        reset_btn.pack(side='left', padx=15)

        quit_btn = tk.Button(control_frame, text="❌ ÇIKIŞ",
                             font=('Arial', 14, 'bold'),
                             bg='#757575', fg='white',
                             activebackground='#616161',
                             padx=20, pady=10,
                             command=self.root.quit)
        quit_btn.pack(side='left', padx=15)

    def play_choice(self, choice):
        """Seçim yapıldığında çağrılan fonksiyon"""
        if self.animation_running:
            return

        self.disable_buttons()
        self.start_animation(choice)

    def start_animation(self, player_choice):
        """Animasyon başlat"""
        self.animation_running = True

        # Animasyon thread'i başlat
        animation_thread = threading.Thread(target=self._animate_choices, args=(player_choice,))
        animation_thread.daemon = True
        animation_thread.start()

    def _animate_choices(self, player_choice):
        """Seçim animasyonu"""
        # Oyuncunun seçimini göster
        self.root.after(0, self._update_player_choice, self.game_service.get_choice_emoji(player_choice))

        # Bilgisayar seçimi animasyonu
        animation_choices = ["🗿", "📄", "✂️"]

        for i in range(15):  # 15 kez değiştir
            emoji = animation_choices[i % 3]
            self.root.after(i * 100, self._update_computer_choice, emoji)

        # Oyunu oyna ve sonucu göster
        self.root.after(1500, self._play_and_show_result, player_choice)

    def _update_player_choice(self, emoji):
        """Oyuncu seçimini güncelle"""
        self.player_choice_label.config(text=emoji)

    def _update_computer_choice(self, emoji):
        """Bilgisayar seçimini güncelle"""
        self.computer_choice_label.config(text=emoji)

    def _play_and_show_result(self, player_choice):
        """Oyunu oyna ve sonucu göster"""
        computer_choice, result = self.game_service.play_round(player_choice)

        # Bilgisayarın gerçek seçimini göster
        self.computer_choice_label.config(text=self.game_service.get_choice_emoji(computer_choice))

        # Sonucu göster
        result_text, result_color = self._get_result_display(result)
        self.result_label.config(text=result_text, fg=result_color)

        # Skoru güncelle
        self.update_score()

        # Butonları tekrar aktif et
        self.root.after(1000, self.enable_buttons)
        self.animation_running = False

    def _get_result_display(self, result):
        """Sonuç görüntüleme metni ve rengi"""
        if result == GameResult.WIN:
            return "🎉 KAZANDIN! 🎉", "#4caf50"
        elif result == GameResult.LOSE:
            return "😔 KAYBETTİN", "#f44336"
        else:
            return "🤝 BERABERE", "#ff9800"

    def update_score(self):
        """Skor ve istatistikleri güncelle"""
        player_score, computer_score = self.game_service.get_score()
        win_rate = self.game_service.get_win_percentage()

        self.player_score_label.config(text=str(player_score))
        self.computer_score_label.config(text=str(computer_score))
        self.win_rate_label.config(text=f"{win_rate:.1f}%")

    def disable_buttons(self):
        """Butonları deaktive et"""
        self.rock_btn.config(state='disabled')
        self.paper_btn.config(state='disabled')
        self.scissors_btn.config(state='disabled')

    def enable_buttons(self):
        """Butonları aktive et"""
        self.rock_btn.config(state='normal')
        self.paper_btn.config(state='normal')
        self.scissors_btn.config(state='normal')

    def reset_game(self):
        """Oyunu sıfırla"""
        self.game_service.reset_game()
        self.update_score()

        # Görüntüyü sıfırla
        self.player_choice_label.config(text="❓")
        self.computer_choice_label.config(text="❓")
        self.result_label.config(text="Seçimini yap!", fg='#4fc3f7')

        self.enable_buttons()


# Main Game Class
class RockPaperScissorsGame:
    """Ana oyun sınıfı"""

    def __init__(self):
        self.root = tk.Tk()
        self.ui = GameUI(self.root)

    def run(self):
        """Oyunu başlat"""
        try:
            print("🎮 Taş Kağıt Makas Oyunu başlatılıyor...")
            print("📋 Oyun Kuralları:")
            print("   🗿 Taş -> Makası yener")
            print("   📄 Kağıt -> Taşı yener")
            print("   ✂️ Makas -> Kağıdı yener")
            print("🎯 İyi eğlenceler!")
            print("-" * 40)

            self.root.mainloop()

        except KeyboardInterrupt:
            print("\n👋 Oyun kapatılıyor...")
        except Exception as e:
            print(f"❌ Hata oluştu: {e}")
        finally:
            print("🔚 Oyun sonlandırıldı.")


def main():
    """Ana fonksiyon"""
    game = RockPaperScissorsGame()
    game.run()


if __name__ == "__main__":
    main()