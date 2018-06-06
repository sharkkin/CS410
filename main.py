#!/usr/bin/env python3
'''
Despit the name containing EVE this is not related to the game produced by CCP (tm)  or EVE (c)
MIT GPL opensource.org

Copyright 2018 Sharkkin

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE
'''



import re


def read_file_ammo():
    ammo = []
    with open("eve_ammo.txt") as file:
        for line in file:
            #strings = re.search('^(.*?):(.*?):(\d+):(\d+):(\d+):(\d+):(\d+):(\d+)', line)
            strings = line.split(':')
            strings[-1] = strings[-1].rstrip()
            if strings:
                var_type = strings[0]
                var_name = strings[1]
                var_mod = strings[2]
                var_EM = strings[3]
                var_Thermal = strings[4]
                var_Kinetic = strings[5]
                var_Explo = strings[6]
                new_ammo = {
                    'catagory': var_type,
                    'name': var_name,
                    'r_mod': var_mod,
                    'em_dmg': var_EM,
                    'therm_dmg': var_Thermal,
                    'kin_dmg': var_Kinetic,
                    'explo': var_Explo,
                }
            ammo.append(new_ammo)
    return ammo

def read_file_wpns():
    weapons = []
    with open("eve_wpns.txt") as file:
        for line in file:
            strings = line.split(':')
            strings[-1] = strings[-1].rstrip()
            if strings:
              var_type = strings[0]
              var_name = strings[1]
              var_optimal = strings[2]
              var_falloff = strings[3]
              var_rate = strings[4]
              var_mod = strings[5]
              new_weapons = {
              'type': var_type,
              'name': var_name,
              'optimal': var_optimal,
              'falloff': var_falloff,
              'rate': var_rate,
              'mod': var_mod,
            }
            weapons.append(new_weapons)
    return weapons

def read_file_skills():
    skills = {}
    with open("eve_skills.txt","rt") as file:
        for line in file:
            strings = re.search('^(.*?)=(\d+)', line)
            if strings:
                var_name = strings.group(1)
                var_skills = strings.group(2)
                new_skills = {
                     var_name: var_skills
                }
                skills[var_name] = var_skills
    return skills

def range_calc(mod_range, mod_optimal, mod_falloff):
    range_check = (mod_range - mod_optimal)
    if range_check <= 0:
        return 1
    else:
        modification = 0# (0.5 * (((mod_range - mod_optimal)/mod_falloff) * ((mod_range - mod_optimal)/mod_falloff) ))
        return modification

def damage_percent(skill,each_ammo, weapon, mod_range):
    mod_optimal = float(each_ammo["r_mod"]) * float(weapon["optimal"])
    mod_falloff = float(each_ammo["r_mod"]) * float(weapon["falloff"])
    dam_p = (1+(float(skill)*0.02)) * range_calc(mod_range, mod_optimal, mod_falloff)
    return dam_p

def damage_calc(each_ammo, weapon, damage_mod):
    total_dmg = (damage_mod * (float(each_ammo["em_dmg"]) + float(each_ammo["therm_dmg"]) + float(each_ammo["kin_dmg"]) + float(each_ammo["explo"]))/float(weapon["rate"]))
    return total_dmg

def proj_wpn(mod_range, skills, ammo, weapons):
    max_wpn_name = None
    max_ammo_name = None
    max_damage = 0
    this_damage = 0
    for weapon in weapons:
        if weapon["type"] == "autocannon":
            for each_ammo in ammo:
                if each_ammo["catagory"] == "proj":
                    damage_mod = damage_percent(skills["Small Autocannon Specialization"], each_ammo, weapon, mod_range)
                    this_damage = damage_calc(each_ammo, weapon, damage_mod)
                if this_damage > max_damage:
                    max_damage = this_damage
                    max_wpn_name = weapon["name"]
                    max_ammo_name = each_ammo["name"]
        if weapon["type"] == "artillery":
            for each_ammo in ammo:
                if each_ammo["catagory"] == "proj":
                    damage_mod = damage_percent(skills["Small Artillery Specialization"], each_ammo, weapon, mod_range)
                    this_damage = damage_calc(each_ammo, weapon, damage_mod)
                if this_damage > max_damage:
                    max_damage = this_damage
                    max_wpn_name = weapon["name"]
                    max_ammo_name = each_ammo["name"]
    print("Best projectile weapon is {0} using {1} for {2} damage per second" .format (max_wpn_name, max_ammo_name,round(max_damage,3)))

def hybrid_wpn(mod_range, skills, ammo, weapons):
    max_wpn_name = None
    max_ammo_name = None
    max_damage = 0
    this_damage = 0
    for weapon in weapons:
        if weapon["type"] == "blaster":
            for each_ammo in ammo:
                if each_ammo["catagory"] == "hybrid":
                    damage_mod = damage_percent(skills["Small Blaster Specialization"], each_ammo, weapon, mod_range)
                    this_damage = damage_calc(each_ammo, weapon, damage_mod)
                if this_damage > max_damage:
                    max_damage = this_damage
                    max_wpn_name = weapon["name"]
                    max_ammo_name = each_ammo["name"]
        if weapon["type"] == "rail":
            for each_ammo in ammo:
                if each_ammo["catagory"] == "hybrid":
                    damage_mod = damage_percent(skills["Small Railgun Specialization"], each_ammo, weapon, mod_range)
                    this_damage = damage_calc(each_ammo, weapon, damage_mod)
                if this_damage > max_damage:
                    max_damage = this_damage
                    max_wpn_name = weapon["name"]
                    max_ammo_name = each_ammo["name"]
    print("Best hybrid weapon is {0} using {1} for {2} damage per second" .format (max_wpn_name, max_ammo_name, round(max_damage,3)))

def laser_wpn(mod_range, skills, ammo, weapons):
    this_damage = 0
    max_damage = 0
    max_wpn_name = None
    max_ammo_name = None
    for weapon in weapons:
        if weapon["type"] == "beam":
            for each_ammo in ammo:
                if each_ammo["catagory"] == "crystals":
                    damage_mod = damage_percent(skills["Small Beam Laser Specialization"], each_ammo, weapon, mod_range)
                    this_damage = damage_calc(each_ammo, weapon, damage_mod)
                if this_damage > max_damage:
                    max_damage = this_damage
                    max_wpn_name = weapon["name"]
                    max_ammo_name = each_ammo["name"]
        if weapon["type"] == "pulse":
            for each_ammo in ammo:
                if each_ammo["catagory"] == "crystals":
                    damage_mod = damage_percent(skills["Small Pulse Laser Specialization"], each_ammo, weapon, mod_range)
                    this_damage = damage_calc(each_ammo, weapon, damage_mod)
                if this_damage > max_damage:
                    max_damage = this_damage
                    max_wpn_name = weapon["name"]
                    max_ammo_name = each_ammo["name"]
    print("Best laser weapon is {0} using {1} for {2} damage per second" .format (max_wpn_name, max_ammo_name, round(max_damage,3)))

def main():
    ammo = read_file_ammo()
    weapons = read_file_wpns()
    skills = read_file_skills()
    input_range = int(input("Enter desired range: "))
    mod_range = input_range * (1 - (0.05 * int(skills["Sharpshooter"])))
    proj_wpn(mod_range, skills, ammo, weapons)
    hybrid_wpn(mod_range, skills, ammo, weapons)
    laser_wpn(mod_range, skills, ammo, weapons)

main()

'''
    gunnery = skills.my_dict.get('Gunnery')# 2% bonus to rate of fire
    rapid_firing = skills.my_dict.get('Rapid Firing')#4% bonus rate of fire
    sharpshooter = skills.my_dict.get('Sharpshooter')# 5% range bonus
    sm_arty_spec = skills.my_dict.get('Small Artillery Specialization')# 2% bonus damage for small artillery
    sm_auto_spec = skills.my_dict.get('Small Autocannon Specialization')#2% bonus
    sm_beam_spec = skills.my_dict.get('Small Beam Laser Specialization')
    sm_blast_spec = skills.my_dict.get('Small Blaster Specialization')
    sm_energy = skills.my_dict.get('Small Energy Turret')
    sm_hybrid = skills.my_dict.get('Small Hybrid Turret')
    sm_project = skills.my_dict.get('Small Projectile Turret')
    sm_laser = skills.my_dict.get('Small Pulse Laser Specialization')
    sm_railgun = skills.my_dict.get('Small Railgun Specialization')
    surgical = skills.my_dict.get('Surgical Strike')
    print("auto",sm_auto_spec)
    print("beam",sm_beam_spec)
    print("blast",sm_blast_spec)
    print("energy",sm_energy)
    print("hybrid",sm_hybrid)
    print("proj",sm_project)
    print("laser",sm_laser)
    print("rail",sm_railgun)
    print("surg",surgical)
    return 
 #   for x in new_weapons.get(ammo_type):
  #    if x optimal >= required_dist:

dictionary.keys

      print("Gunnery %s" % str(skills["Gunnery"]))
      print("Rap %s" % str(skills["Rapid Firing"]))
      print(weapons)

'''
