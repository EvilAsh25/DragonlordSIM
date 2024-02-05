#!/usr/bin/env python3

import time
import os
import csv
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename
import battle

# Stats [S HP, S MP, ATK, DEF, STR, AGI, MAX HP, MAX MP, Armor(0, 1, 2)]
hero = battle.HeroStats(0, 0, 0, 0, 0, 0, 0, 0, 0)

# Enemy Stats [HP, ATK, AGI]
dragonlord2 = battle.EnemyStats("Dragonlord 2", 130, 140, 200)

# Combobox to Equipment Stats
weapon = {0: 0, 1: 2, 2: 4, 3: 10, 4: 15, 5: 20, 6: 28, 7: 40}
armor = {0: 0, 1: 2, 2: 4, 3: 10, 4: 16, 5: 24, 6: 24, 7: 28}
armor_type = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 1, 7: 2}
shield = {0: 0, 1: 4, 2: 10, 3: 20}

# Base Stats based on Level
strength = {1:4, 2:5, 3:7, 4:7, 5:12, 6:16, 7:18, 8:22, 9:30, 10:35, 11:40, 12:48, 13:52, 14:60, 15:68, 16:72, 17:72,
            18:85, 19:87, 20:92, 21:95, 22:97, 23:99, 24:103, 25:113, 26:117, 27:125, 28:130, 29:135, 30:140}
agility = {1:4, 2:4, 3:6, 4:8, 5:10, 6:10, 7:17, 8:20, 9:22, 10:31, 11:35, 12:40, 13:48, 14:55, 15:64, 16:70, 17:78,
           18:84, 19:86, 20:88, 21:90, 22:90, 23:94, 24:98, 25:100, 26:105, 27:107, 28:115, 29:120, 30:130}
HP = {1:15, 2:22, 3:24, 4:31, 5:35, 6:38, 7:40, 8:46, 9:50, 10:54, 11:62, 12:63, 13:70, 14:78, 15:86, 16:92, 17:100,
      18:115, 19:130, 20:138, 21:149, 22:158, 23:165, 24:170, 25:174, 26:180, 27:189, 28:195, 29:200, 30:210}
MP = {1:0, 2:0, 3:5, 4:16, 5:20, 6:24, 7:26, 8:29, 9:36, 10:40, 11:50, 12:58, 13:64, 14:70, 15:72, 16:95, 17:100,
      18:108, 19:115, 20:128, 21:135, 22:146, 23:153, 24:161, 25:161, 26:168, 27:175, 28:180, 29:190, 30:200}

def simulate_basic():
    # Check that all the inputs are valid
    if entry_sim.get().isdigit() and entry_startHP.get().isdigit() and entry_startMP.get().isdigit() and entry_healThresh.get().isdigit():
        hero.startHP = int(entry_startHP.get())
        hero.startMP = int(entry_startMP.get())
        healmore_threshold = int(entry_healThresh.get())
        writeToLog(f'---------------- Level: {combo_level.get()} [{combo_name.get().split()[0]}] ----------------')
        writeToLog(f'-- HP:{hero.maxHP} | MP:{hero.maxMP} | ATK:{hero.ATK} | DEF:{hero.DEF} | AGI:{hero.AGI} --')
        writeToLog(f'-- Start HP:{hero.startHP} | Start MP:{hero.startMP} | Heal@:{healmore_threshold} --\n')
        writeToLog(f'------ Running {int(entry_sim.get())} trials ------')
        button_sim.config(text="Running Simulation...", )
        button_sim['state'] = 'disabled'
        window.update()
        start_time = time.time()
        text, data = battle.enemy_battle(hero, dragonlord2, int(entry_sim.get()), healmore_threshold, True)
        writeToLog(text)
        writeToLog(f'\n----------- Execution time: {round((time.time() - start_time), 2)} seconds -----------\n')
        button_sim.config(text="Simulate Single")
        button_sim['state'] = 'normal'
    else:
        writeToLog('Invalid entry')

def simulate_advanced():
    # Check that all the inputs are valid
    if entry_sim.get().isdigit() and entry_startHP.get().isdigit() and entry_startMP.get().isdigit() and \
            entry_healThresh.get().isdigit() and entry_startHP2.get().isdigit() and entry_startMP2.get().isdigit() and \
            entry_healThresh2.get().isdigit():

        filename = tk.filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save CSV File",
                                                   filetypes=[('CSV File', '*.csv')], defaultextension='.csv')
        if filename:
            writeToLog(f'------------------ Level: {combo_level.get()} [{combo_name.get().split()[0]}] ------------------')
            writeToLog(f'---- HP:{hero.maxHP} | MP:{hero.maxMP} | ATK:{hero.ATK} | DEF:{hero.DEF} | AGI:{hero.AGI} ----\n')

            startHP_range = int(entry_startHP2.get()) - int(entry_startHP.get())
            startMP_range = int(entry_startMP2.get()) - int(entry_startMP.get())
            startHeal_range = int(entry_healThresh2.get()) - int(entry_healThresh.get())
            if startHP_range < 0:
                startHP_range = 0
            if startMP_range < 0:
                startMP_range = 0
            if startHeal_range < 0:
                startHeal_range = 0
            total_sims = (startHP_range+1)*(startMP_range+1)*(startHeal_range+1)

            # tot_wins, tot_atk, tot_damage, tot_win_rounds, tot_lose_rounds, tot_preempt, tot_preempt_wins, pre_death
            full_data = [[f'Level: {combo_level.get()} [{combo_name.get().split()[0]}] | HP:{hero.maxHP} | MP:{hero.maxMP} |'
                          f' ATK:{hero.ATK} | DEF:{hero.DEF} | AGI:{hero.AGI}'],
                         ['Trials', entry_sim.get()],
                         ['Start HP', 'Start MP', 'Heal@', "Wins", "Total Attacks Wins", "Total Damage Wins",
                          "Total Rounds Wins", "Total Rounds Losses", "Total Enemy First", "Total Enemy First Wins",  "Premature Deaths"]]
            writeToLog(f'----------- Running {total_sims} x {int(entry_sim.get())} trials -----------')
            button_sim2.config(text="Running Simulation...", )
            button_sim2['state'] = 'disabled'
            start_time = time.time()

            # Loop through all the Sims
            for x in range(startHP_range+1):
                hero.startHP = int(entry_startHP.get()) + x
                for y in range(startMP_range+1):
                    hero.startMP = int(entry_startMP.get()) + y
                    for z in range(startHeal_range+1):
                        healmore_threshold = int(entry_healThresh.get()) + z
                        writeToLog(f'-- Start HP:{hero.startHP} | Start MP:{hero.startMP} | Heal@:{healmore_threshold} --')
                        window.update()
                        text, data = battle.enemy_battle(hero, dragonlord2, int(entry_sim.get()), healmore_threshold, True)
                        data.insert(0, hero.startHP)
                        data.insert(1, hero.startMP)
                        data.insert(2, healmore_threshold)
                        writeToLog(data)
                        full_data.append(data)

            writeToLog(f'\nResults saved in: {filename}')
            writeToLog(f'------------- Execution time: {round((time.time() - start_time), 2)} seconds -------------\n')
            button_sim2.config(text="Simulate Multi")
            button_sim2['state'] = 'normal'
            writeCSV(full_data, filename)

    else:
        writeToLog('Invalid entry')
    return

def updateStatsCallback(event):
    # Read Comboboxes and build stats
    # Stats [S HP, S MP, ATK, DEF, STR, AGI, MAX HP, MAX MP]
    level = int(combo_level.get())
    name = combo_name.current()
    # ["STR+HP [d,t,J,Z]", "STR+AGI [f,v,L,(]", "HP+AGI", "STR+MP", "AGI+MP", "HP+MP"]
    if name == 0 or name == 1 or name == 3:
        hero.STR = strength.get(level)
    else:
        hero.STR = strength.get(level)*9//10 + 3
    if name == 1 or name == 2 or name == 4:
        hero.AGI = agility.get(level)
    else:
        hero.AGI = agility.get(level) * 9 // 10 + 3
    if name == 0 or name == 2 or name == 5:
        hero.maxHP = HP.get(level)
    else:
        hero.maxHP = HP.get(level)*9//10 + 3
    if name == 3 or name == 4 or name == 5:
        hero.maxMP = MP.get(level)
    else:
        hero.maxMP = MP.get(level)*9//10 + 3

    # Update Stats based on Selected Weapons/Armor
    hero.ATK = hero.STR + weapon.get(combo_weapon.current(), 0)
    hero.DEF = (hero.AGI//2) + armor.get(checkDS.get(), 0) + armor.get(combo_armor.current(), 0) + shield.get(combo_shield.current(), 0)
    hero.armorType = armor_type.get(combo_armor.current())

    # Update all the Labels for new stats
    labelHP.set(f'HP: {hero.maxHP}')
    labelMP.set(f'MP: {hero.maxMP}')
    labelSTR.set(f'STR: {hero.STR}')
    labelAGI.set(f'AGI: {hero.AGI}')
    labelATK.set(f'ATK: {hero.ATK}')
    labelDEF.set(f'DEF: {hero.DEF}')
    entry_startHP.delete(0, tk.END)
    entry_startHP.insert(0, hero.maxHP)
    entry_startHP2.delete(0, tk.END)
    entry_startHP2.insert(0, hero.maxHP)
    entry_startMP.delete(0, tk.END)
    entry_startMP.insert(0, hero.maxMP)
    entry_startMP2.delete(0, tk.END)
    entry_startMP2.insert(0, hero.maxMP)
    # Set Heal Threshold to max possible damage
    entry_healThresh.delete(0, tk.END)
    entry_healThresh2.delete(0, tk.END)
    if battle.max_damage(dragonlord2.ATK, hero.DEF) > battle.max_damage_breath(1, hero.armorType):
        entry_healThresh.insert(0, battle.max_damage(dragonlord2.ATK, hero.DEF))
        entry_healThresh2.insert(0, battle.max_damage(dragonlord2.ATK, hero.DEF))
    else:
        entry_healThresh.insert(0, battle.max_damage_breath(1, hero.armorType))
        entry_healThresh2.insert(0, battle.max_damage_breath(1, hero.armorType))
    labelEnemyName.set(f'{dragonlord2.name} Stats')
    labelEnemyHP.set(f'HP: {dragonlord2.maxHP}')
    labelEnemyATK.set(f'ATK: {dragonlord2.ATK}')
    labelEnemyAGI.set(f'AGI: {dragonlord2.AGI}')
    labelEnemyInitiative.set(f'Enemy Goes First: {round(battle.enemy_initiative(hero.AGI, dragonlord2.AGI)*100, 2)}%')
    labelEnemyDMGGiven.set(f'Damage Given: {battle.min_damage(hero.ATK, dragonlord2.AGI)}...{battle.max_damage(hero.ATK, dragonlord2.AGI)}')
    labelEnemyDMGPhysical.set(f'Physical Taken: {battle.min_damage(dragonlord2.ATK, hero.DEF)}...{battle.max_damage(dragonlord2.ATK, hero.DEF)}')
    labelEnemyDMGBreath.set(f'Breath Taken: {battle.min_damage_breath(1, hero.armorType)}...{battle.max_damage_breath(1, hero.armorType)}')

def checkboxCallback():
    updateStatsCallback(event=0)

def saveFile():
    filename = tk.filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save File",
                                               filetypes=[('Text File', '*.txt')], defaultextension='.txt')
    if filename:
        f = open(filename, 'w')
        f.write(output_log.get(1.0, 'end'))
        f.close()

def writeCSV(data, filename):

    if filename:
        f = open(filename, 'w', newline='')
        writer = csv.writer(f)
        writer.writerows(data)

# Taken from https://tkdocs.com/tutorial/text.html
def writeToLog(msg):
    output_log['state'] = 'normal'
    if output_log.index('end-1c') != '1.0':
        output_log.insert('end', '\n')
    output_log.insert('end', msg)
    output_log['state'] = 'disabled'
    output_log.see("end")

def clearLog():
    output_log['state'] = 'normal'
    output_log.delete(1.0, tk.END)
    output_log['state'] = 'disabled'

# Create GUI Window
window = tk.Tk()
window.title("Dragonlord 2 Simulator")
window.geometry("980x600")
window.minsize(980, 600)

# Weight configuration (window sizing)
window.columnconfigure(2, weight=1)
window.rowconfigure(4, weight=1)

# Frames
character_entry_frame = tk.Frame(window, borderwidth=1, relief="ridge")
character_entry_frame.grid(column=0, row=0, pady=(20, 0), padx=20, ipady=4, ipadx=4, sticky="nw")
#character_stats_frame = tk.Frame(window)
#character_stats_frame.grid(column=1, row=0, pady=20, padx=20, sticky="n")
data_frame = tk.Frame(window, borderwidth=1, relief="ridge")
data_frame.grid(column=1, row=0, pady=20, padx=(0, 20), ipady=0, ipadx=0, sticky="news", rowspan=2)
simulate_frame = tk.Frame(window, borderwidth=1, relief="ridge")
simulate_frame.grid(column=0, row=1, pady=(20, 20), padx=(20, 20), ipady=0, ipadx=0, rowspan=2)
button_frame = tk.Frame(window, borderwidth=1, relief="ridge")
button_frame.grid(column=1, row=3, pady=(0, 20), padx=(0, 20), ipady=0, ipadx=0)

# Character Combobox
tk.Label(character_entry_frame, text="Name:").grid(column=0, row=0, pady=(5,0))
combo_name = ttk.Combobox(character_entry_frame, values=["STR+HP [d,t,J,Z]", "STR+AGI [f,v,L,(]", "HP+AGI", "STR+MP", "AGI+MP", "HP+MP"])
combo_name.current(0)
combo_name.grid(column=1, row=0, pady=(10, 5), columnspan=2)
combo_name.bind("<<ComboboxSelected>>", updateStatsCallback)

# Level Combobox
tk.Label(character_entry_frame, text="Level:").grid(column=0, row=1)
combo_level = ttk.Combobox(character_entry_frame,
                           values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15","16",
                                   "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"])
combo_level.current(17)
combo_level.grid(column=1, row=1, pady=5, columnspan=2)
combo_level.bind("<<ComboboxSelected>>", updateStatsCallback)

# Weapon Combobox
tk.Label(character_entry_frame, text="Weapon:").grid(column=0, row=2)
combo_weapon = ttk.Combobox(character_entry_frame,
                            values=["(none)", "Bamboo Pole (+2)", "Club (+4)", "Copper Sword (+10)", "Hand Axe (+15)",
                                    "Broad Sword (+20)", "Flame Sword (+28)", "Erdrick's Sword (+40)"])
combo_weapon.current(7)
combo_weapon.grid(column=1, row=2, pady=5, columnspan=2)
combo_weapon.bind("<<ComboboxSelected>>", updateStatsCallback)

# Armor Combobox
tk.Label(character_entry_frame, text="Armor:").grid(column=0, row=3)
combo_armor = ttk.Combobox(character_entry_frame,
                           values=["(none)", "Clothes (+2)", "Leather Armor (+4)", "Chain Mail (+10)",
                                   "Half Plate (+16)", "Full Plate (+24)", "Magic Armor (+24)",
                                   "Erdrick's Armor (+28)"])
combo_armor.current(7)
combo_armor.grid(column=1, row=3, pady=5, columnspan=2)
combo_armor.bind("<<ComboboxSelected>>", updateStatsCallback)

# Shield Combobox
tk.Label(character_entry_frame, text="Shield:").grid(column=0, row=4)
combo_shield = ttk.Combobox(character_entry_frame,
                            values=["(none)", "Small Shield (+4)", "Large Shield (+10)", "Silver Shield (+20)"])
combo_shield.current(3)
combo_shield.grid(column=1, row=4, pady=5, columnspan=2)
combo_shield.bind("<<ComboboxSelected>>", updateStatsCallback)

# Dragon Scale Checkbox
checkDS = tk.IntVar()
check_scale = tk.Checkbutton(character_entry_frame, text="Dragon Scale (+2)", variable=checkDS, command=checkboxCallback)
check_scale.grid(column=0, row=5, pady=5, columnspan=2)
check_scale.select()

# Starting HP Entry
label_startHP = tk.Label(character_entry_frame, text="Starting HP:").grid(column=0, row=6)
entry_startHP = tk.Entry(character_entry_frame, width=8)
entry_startHP.grid(column=1, row=6, pady=5)
entry_startHP2 = tk.Entry(character_entry_frame, width=8)
entry_startHP2.grid(column=2, row=6, pady=5)

# Starting MP Entry
label_startMP = tk.Label(character_entry_frame, text="Starting MP:").grid(column=0, row=7)
entry_startMP = tk.Entry(character_entry_frame, width=8)
entry_startMP.grid(column=1, row=7, pady=5)
entry_startMP2 = tk.Entry(character_entry_frame, width=8)
entry_startMP2.grid(column=2, row=7, pady=5)

# Heal Threshold Entry
label_healThresh = tk.Label(character_entry_frame, text="Heal Threshold:").grid(column=0, row=8)
entry_healThresh = tk.Entry(character_entry_frame, width=8)
entry_healThresh.grid(column=1, row=8, pady=5)
entry_healThresh2 = tk.Entry(character_entry_frame, width=8)
entry_healThresh2.grid(column=2, row=8, pady=5)

# Number of Simulations Entry
label_sim = tk.Label(simulate_frame, text="# of Simulations", font='bold').grid(column=0, row=0, pady=(5,0))
entry_sim = tk.Entry(simulate_frame)
entry_sim.grid(column=0, row=1, pady=(5, 0), padx=(20, 20))
entry_sim.insert(0, "10000")

# Simulate Button
button_sim = tk.Button(simulate_frame, text="Simulate Single", command=simulate_basic)
button_sim.grid(column=0, row=2, pady=(10,10))

# Simulate 2 Button
#labelSIM2 = tk.StringVar()
#tk.Label(simulate_frame, textvariable=labelSIM2, font='bold').grid(column=0, row=3, pady=(5,0))
button_sim2 = tk.Button(simulate_frame, text="Simulate Multi", command=simulate_advanced)
button_sim2.grid(column=0, row=5, pady=(0,10), columnspan=1)

# Hero Stats Labels
labelHP = tk.StringVar()
labelMP = tk.StringVar()
labelSTR = tk.StringVar()
labelAGI = tk.StringVar()
labelATK = tk.StringVar()
labelDEF = tk.StringVar()
tk.Label(data_frame, text="Hero Stats", font='bold').grid(column=0, row=1, pady=(6,0))
tk.Label(data_frame, textvariable=labelHP).grid(column=0, row=2)
tk.Label(data_frame, textvariable=labelMP).grid(column=0, row=3)
tk.Label(data_frame, textvariable=labelSTR).grid(column=0, row=4)
tk.Label(data_frame, textvariable=labelAGI).grid(column=0, row=5)
tk.Label(data_frame, textvariable=labelATK).grid(column=0, row=6)
tk.Label(data_frame, textvariable=labelDEF).grid(column=0, row=7)
tk.Label(data_frame, text=" ").grid(column=0, row=8, padx=80)

# Enemy Stats
labelEnemyName = tk.StringVar()
labelEnemyHP = tk.StringVar()
labelEnemyATK = tk.StringVar()
labelEnemyAGI = tk.StringVar()
labelEnemyDMGGiven = tk.StringVar()
labelEnemyDMGPhysical = tk.StringVar()
labelEnemyDMGBreath = tk.StringVar()
labelEnemyInitiative = tk.StringVar()
tk.Label(data_frame, textvariable=labelEnemyName, font='bold').grid(column=0, row=9)
tk.Label(data_frame, textvariable=labelEnemyHP).grid(column=0, row=10)
tk.Label(data_frame, textvariable=labelEnemyATK).grid(column=0, row=11)
tk.Label(data_frame, textvariable=labelEnemyAGI).grid(column=0, row=12)
tk.Label(data_frame, text=" ").grid(column=0, row=13, padx=80)
tk.Label(data_frame, text="Battle Data", font='bold').grid(column=0, row=14, pady=(0,0))
tk.Label(data_frame, textvariable=labelEnemyInitiative).grid(column=0, row=15)
tk.Label(data_frame, textvariable=labelEnemyDMGGiven).grid(column=0, row=16)
tk.Label(data_frame, textvariable=labelEnemyDMGPhysical).grid(column=0, row=17)
tk.Label(data_frame, textvariable=labelEnemyDMGBreath).grid(column=0, row=18)

# Clear Button
button_clear = tk.Button(button_frame, text="Clear", command=clearLog)
button_clear.grid(column=0, row=0, pady=(10, 10), padx=(20, 10))

# Save Button
button_quit = tk.Button(button_frame, text="Save", width=8, command=saveFile)
button_quit.grid(column=1, row=0, pady=10, padx=10, sticky="", columnspan=1)

# Quit Button
button_quit = tk.Button(button_frame, text="Quit", width=8, command=window.destroy)
button_quit.grid(column=0, row=1, sticky="",pady=10, padx=10, columnspan=2)

# Textbox Output Log
output_log = tk.Text(window, state='disabled', width=60, height=30, wrap='none')
output_log_vs = ttk.Scrollbar(window, orient='vertical', command=output_log.yview)
output_log['yscrollcommand'] = output_log_vs.set
output_log.grid(column=2, row=0, padx=0, pady=(20, 10), sticky="news", rowspan=5)
output_log_vs.grid(column=3, row=0, pady=20, sticky="news", rowspan=5)


#Main
updateStatsCallback(event=0)
window.mainloop()

# Test Randomness functions
'''
dmg_array = np.array([])
agi = 18
for x in range(10000):
    dmg = battle.enemy_initiative_test(agi, 50)
    #dmg = enemy_initiative(hero.STR, 200)
    #dmg = enemy_attack(hero.ATK, 200)
    dmg_array = np.append(dmg_array, dmg)
unique, counts = np.unique(dmg_array, return_counts=True)
print(dict(zip(unique, counts)))
print(battle.enemy_initiative(agi, 200))
'''
