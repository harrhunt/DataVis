import json
import os
from bokeh.plotting import figure, show
from bokeh.transform import jitter
from bokeh.models import ColumnDataSource


def visualize_spells():
    schools_data = {}
    spell_list = os.listdir("data/spells")
    for spell_name in spell_list:
        with open(f"data/spells/{spell_name}", "r") as file:
            spell_data = json.load(file)
        spell_school = spell_data["school"]["name"]
        if spell_school not in schools_data:
            schools_data[spell_school] = 1
        else:
            schools_data[spell_school] += 1
    schools = []
    counts = []
    for k, v in schools_data.items():
        schools.append(k)
        counts.append(v)
    sorted_schools = sorted(schools, key=lambda x: counts[schools.index(x)], reverse=True)
    p = figure(x_range=sorted_schools, title="Number of Spells by School of Magic", x_axis_label="School of Magic",
               y_axis_label="Number of Spells", width=750)
    p.vbar(x=schools, top=counts, legend_label="Number of Spells", width=0.5, bottom=0, color="red")
    p.xgrid.grid_line_color = None
    show(p)


def visualize_monster_alignment():
    to_skip = ["any alignment", "unaligned", "any non-good alignment", "any non-lawful alignment", "any chaotic alignment", "any evil alignment"]
    ethics_values = ["Chaotic", "Neutral", "Lawful"]
    morals_values = ["Evil", "Neutral", "Good"]
    totals = {"Chaotic Evil": 0, "Chaotic Neutral": 0, "Chaotic Good": 0, "Neutral Evil": 0, "Neutral Neutral": 0,
              "Neutral Good": 0, "Lawful Evil": 0, "Lawful Neutral": 0, "Lawful Good": 0}
    ethics = []
    morals = []
    names = []
    challenge_rating = []
    ethics_totals = []
    morals_totals = []
    count_totals = []
    monster_list = os.listdir("data/monsters")
    for monster_name in monster_list:
        with open(f"data/monsters/{monster_name}", "r") as file:
            monster_data = json.load(file)
        monster_alignment = monster_data["alignment"]
        if monster_alignment in to_skip:
            continue
        ethic_and_moral = monster_alignment.title().split()
        if len(ethic_and_moral) == 1:
            ethics.append(ethic_and_moral[0])
            morals.append(ethic_and_moral[0])
            totals[f"{ethic_and_moral[0]} {ethic_and_moral[0]}"] += 1
        else:
            ethics.append(ethic_and_moral[0])
            morals.append(ethic_and_moral[1])
            totals[f"{ethic_and_moral[0]} {ethic_and_moral[1]}"] += 1
        names.append(monster_data["name"])
        challenge_rating.append((monster_data["challenge_rating"] + 1) * 3)

    for k, v in totals.items():
        ethics_totals.append(k.split()[0])
        morals_totals.append(k.split()[1])
        count_totals.append(v*3)

    source = ColumnDataSource(data=dict(ethics=ethics, morals=morals, names=names, challenge_rating=challenge_rating))
    source_totals = ColumnDataSource(data=dict(ethics=ethics_totals, morals=morals_totals, count=count_totals))
    p = figure(x_range=ethics_values, y_range=morals_values)
    p.circle(x=jitter('ethics', width=0.3, range=p.x_range), y=jitter('morals', width=0.3, range=p.y_range),
             source=source, alpha=0.3, color="orange", size='challenge_rating')
    p.circle(x='ethics', y='morals', source=source_totals, alpha=0.2, color="red", size='count')
    p.hover.tooltip = [
        ("index", "$index"),
        ("(x,y)", "($x, $y)"),
        ("radius", "@radius"),
        ("fill color", "$color[hex, swatch]:fill_color"),
        ("fill color", "$color[hex]:fill_color"),
        ("fill color", "$color:fill_color"),
        ("fill color", "$swatch:fill_color"),
        ("foo", "@foo"),
        ("bar", "@bar"),
        ("baz", "@baz{safe}"),
        ("total", "@total{$0,0.00}")
    ]
    show(p)


if __name__ == '__main__':
    # visualize_spells()
    visualize_monster_alignment()
