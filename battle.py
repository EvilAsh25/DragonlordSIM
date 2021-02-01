#!/usr/bin/env python3

import numpy as np
import recordtype as rt
from collections import namedtuple

rng = np.random.default_rng()
HeroStats = rt.recordtype('HeroStats', ['startHP', 'startMP', 'ATK', 'DEF', 'STR', 'AGI', 'maxHP', 'maxMP', 'armorType'])
EnemyStats = namedtuple('EnemyStats', ['name', 'maxHP', 'ATK', 'AGI'])

# returns value between 0 to max_rng
def get_rng(min_rng, max_rng):
    return rng.integers(min_rng, max_rng + 1)

def max_damage(attack, defense):
    base = attack - (defense // 2)
    dmg = (((base + 1) * 255) // 256 + base) // 4
    if dmg < 1:
        return 1
    else:
        return dmg

def min_damage(attack, defense):
    base = attack - (defense // 2)
    dmg = (((base + 1) * 0) // 256 + base) // 4
    if dmg < 0:
        return 0
    else:
        return dmg

def min_damage_breath(breath, armor):
    damage = 0
    if breath == 1:
        damage = 65
    else:
        damage = 16
    if armor == 2:
        return (damage//3)*2
    else:
        return damage

def max_damage_breath(breath, armor):
    damage = 0
    if breath == 1:
        damage = 72
    else:
        damage = 23
    if armor == 2:
        return (damage // 3) * 2
    else:
        return damage

def enemy_attack(attack, defense, seed=255):
    base = attack - (defense // 2)
    return (((base + 1) * get_rng(0, 255)) // 256 + base) // 4

def enemy_breath(breath, armor):
    damage = 0
    # Type 0-weak, 1-strong
    if breath == 1:
        damage = get_rng(65, 72)
    else:
        damage = get_rng(16, 23)
    if armor == 2:
        return (damage//3)*2
    else:
        return damage

def hero_attack(attack, agility):
    base = attack - (agility // 2)
    return (((base + 1) * get_rng(0, 255)) // 256 + base) // 4

def enemy_initiative(hero_agi, enemy_agi):
    e_agi = enemy_agi//4
    if hero_agi >= e_agi:
        return (1 - ((hero_agi - e_agi) / hero_agi)) / 2
    else:
        return 1 - ((1 - ((e_agi - hero_agi) / e_agi)) / 2)

def enemy_initiative_test(hero_agi, enemy_agi):
    return (hero_agi * get_rng(0, 255)) <= (enemy_agi * get_rng(0, 63))

def random_test(hero_agi, enemy_agi):
    return (hero_agi * get_rng(0, 255)) <= (enemy_agi * get_rng(0, 255))

def enemy_battle(hero_stats, enemy_stats, trials, heal_threshold, smart):
    # Enemy Stats [HP, ATK, AGI]
    # Hero Stats [S HP, S MP, ATK, DEF, STR, AGI, MAX HP, MAX MP, ARMOR]
    returnString = ""
    tot_wins = tot_win_rounds = tot_lose_rounds = pre_death = tot_preempt = tot_preempt_wins = tot_atk = 0
    tot_damage = round_damage = 0
    preempt = preempt_track = False
    verbose = True
    if trials > 1: verbose = False

    for x in range(trials):
        hero_hp = hero_stats.startHP
        hero_mp = hero_stats.startMP
        enemy_hp = enemy_stats.maxHP
        rounds = hero_atk = round_damage = 0
        preempt_track = False
        if verbose: returnString += f'Battle {x+1} starting...\n'

        # Check if Dragonlord strikes first
        if enemy_initiative_test(hero_stats.AGI, enemy_stats.AGI):
            preempt = True
            preempt_track = True
            tot_preempt += 1

        while (hero_hp > 0) and (enemy_hp > 0):
            if verbose: returnString += f'[[Hero: HP: {hero_hp} MP: {hero_mp}], [Dragonlord 2: HP: {enemy_hp}]]\n'
            # Hero's Turn
            # Check for preempt
            if not preempt:
                rounds += 1
                # Choose to either Heal or attack, also check if enemy is almost dead
                if ((hero_hp < (heal_threshold+1)) and (hero_mp > 9)) and not \
                        (smart and enemy_hp <= min_damage(hero_stats.ATK, enemy_stats.AGI)):
                    # Healmore
                    hero_mp -= 10
                    heal = get_rng(85, 101)  # Healmore range is 85 to 100
                    # Check if it hits max HP
                    if (hero_hp + heal) > hero_stats.maxHP:
                        heal = hero_stats.maxHP - hero_hp
                    hero_hp += heal
                    if verbose: returnString += f'Hero casts HEALMORE for {heal} HP\n'
                else:
                    # Attack
                    hero_dmg = hero_attack(hero_stats.ATK, enemy_stats.AGI)
                    enemy_hp -= hero_dmg
                    round_damage += hero_dmg
                    hero_atk += 1
                    if verbose: returnString += f'Hero attacks! {hero_dmg}\n'
                    if enemy_hp <= 0:
                        if verbose: returnString += f'Hero wins!\n'
                        break
            # Dragonlord's Turn
            # Determine if Fire Breath or Physical (50/50)
            if preempt:
                preempt = False
                if verbose: returnString += f'Dragonlord goes first!\n'
            if get_rng(0, 1):
                enemy_dmg = enemy_attack(enemy_stats.ATK, hero_stats.DEF)
                if verbose: returnString += f'Dragonlord Attacks! {enemy_dmg}\n'
            else:
                enemy_dmg = enemy_breath(1, hero_stats.armorType)
                if verbose: returnString += f'Dragonlord breaths fire! {enemy_dmg}\n'
            hero_hp -= enemy_dmg
            if hero_hp <= 0:
                if verbose: returnString += f'Thou art dead.\n'
                break
        if verbose: returnString += f'Total rounds: {rounds}\n'
        # Gather Stats
        if enemy_hp <= 0:
            tot_wins += 1
            tot_atk += hero_atk
            tot_damage += round_damage
            tot_win_rounds += rounds
            if preempt_track:
                tot_preempt_wins += 1
        else:
            tot_lose_rounds += rounds
            if hero_mp > 9:
                pre_death += 1
    # Print Stats
    # tot_wins, tot_atk, tot_damage, tot_win_rounds, tot_lose_rounds, tot_preempt, tot_preempt_wins, pre_death
    returnData = [tot_wins, tot_atk, tot_damage, tot_win_rounds, tot_lose_rounds, tot_preempt, tot_preempt_wins, pre_death]
    if not verbose:
        total_losses = trials - tot_wins
        returnString += f'Hero wins {round((tot_wins/trials)*100, 2)}% of the time [{tot_wins}/{trials}]\n'
        if tot_preempt:
            returnString += f'Wins after DL2 went first: {round(tot_preempt_wins / tot_preempt * 100, 2)}% [{tot_preempt_wins}/{tot_preempt}]\n'
            returnString += f'Wins after Hero went first: {round((tot_wins-tot_preempt_wins) / (trials-tot_preempt) * 100, 2)}% [{(tot_wins-tot_preempt_wins)}/{(trials-tot_preempt)}]\n'
        if total_losses: returnString += f'Premature deaths {round(((pre_death / total_losses) * 100), 2)}% [{pre_death}/{total_losses}] of losses\n'
        if tot_wins:
            returnString += f'Avg damage/hit in wins: {round((tot_damage / tot_wins) / (tot_atk / tot_wins), 2)}\n'
            returnString += f'Avg rounds in wins: {round(tot_win_rounds / tot_wins, 2)}\n'
            returnString += f'Avg attacks in wins: {round(tot_atk / tot_wins, 2)}\n'
        if total_losses: returnString += f'Avg rounds in losses: {round(tot_lose_rounds / total_losses, 2)}'
    return returnString, returnData
