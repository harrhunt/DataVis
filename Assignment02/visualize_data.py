import json
import os
from bokeh.plotting import figure, show, output_file
from bokeh.transform import jitter, factor_cmap
from bokeh.layouts import layout
from bokeh.models import ColumnDataSource, LinearInterpolator, WheelZoomTool, Toggle
from bokeh.embed import file_html
from bokeh.palettes import Category10
from bokeh.io import export_png

HTML_TEMPLATE = """{% from macros import embed %}
<!DOCTYPE html>
<html lang="en">
  {% block head %}
  <head>
    {% block inner_head %}
      <meta charset="utf-8">
      <title>{% block title %}{{ title | e if title else "Bokeh Plot" }}{% endblock %}</title>
      {% block preamble %}{% endblock %}
      {% block resources %}
        <style>{{ css_styles }}</style>
        {% block css_resources %}
          {{ bokeh_css | indent(8) if bokeh_css }}
        {% endblock %}
        {% block js_resources %}
          {{ bokeh_js | indent(8) if bokeh_js }}
        {% endblock %}
      {% endblock %}
      {% block postamble %}{% endblock %}
    {% endblock %}
  </head>
  {% endblock %}
  {% block body %}
  <body>
    {% block inner_body %}
      {% block contents %}
        {% for doc in docs %}
          {{ embed(doc) if doc.elementid }}
          {% for root in doc.roots %}
            {% block root scoped %}
              {{ embed(root) | indent(10) }}
            {% endblock %}
          {% endfor %}
        {% endfor %}
        <div class='caption'>{{ caption }}</div>
      {% endblock %}
      {{ plot_script | indent(8) }}
    {% endblock %}
  </body>
  {% endblock %}
</html>"""

CSS_STYLES = """.caption {width: 750px; font-family: sans-serif; margin-top: 25px;}"""


def save_html(filename, data):
    with open(filename, "w") as file:
        file.write(data)


def visualize_spells_schools(to_png=False):
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

    filename = "Spells_Schools.html"

    caption = """Graph of the number of spells that fall within each school of magic. The school of magic determines the
    characteristics of the spell and what realm of reality they typically affect. For a reference as to what each school
    of magic is and what it affects, refer to this website
    <a href='https://thealpinedm.com/dnd-5e-schools-of-magic/'>https://thealpinedm.com/dnd-5e-schools-of-magic/</a>."""

    if to_png:
        export_png(p, filename=f"{filename.split('.')[0]}.png")
    else:
        save_html(filename, file_html(p, template=HTML_TEMPLATE, resources="cdn", title=p.title.text,
                                      template_variables={"caption": caption, "css_styles": CSS_STYLES}))


def visualize_spell_components_and_types(to_png=False):
    # x_range = ["All Spells", "Verbal", "Somatic", "Material", "Ritual", "Concentration"]
    vsm = {"V": "Verbal", "S": "Somatic", "M": "Material"}
    x_data = {"All Spells": 0, "Verbal": 0, "Somatic": 0, "Material": 0, "Ritual": 0, "Concentration": 0}
    colors = ["red", "green", "green", "green", "blue", "orange"]
    spell_list = os.listdir("data/spells")
    for spell_name in spell_list:
        with open(f"data/spells/{spell_name}", "r") as file:
            spell_data = json.load(file)
        components = spell_data["components"]
        for component in components:
            x_data[vsm[component]] += 1
        x_data["Ritual"] += int(spell_data["ritual"])
        x_data["Concentration"] += int(spell_data["concentration"])
        x_data["All Spells"] += 1
    x = []
    counts = []
    for k, v in x_data.items():
        x.append(k)
        counts.append(v)
    sorted_x = sorted(x, key=lambda a: counts[x.index(a)], reverse=True)
    p = figure(x_range=sorted_x, title="Number of Spells by Components Required, Concentration, and Ritual",
               x_axis_label="Components Required, Concentration, and Ritual",
               y_axis_label="Number of Spells", width=750)
    p.vbar(x=x, top=counts, width=0.5, bottom=0, color=colors)
    p.xgrid.grid_line_color = None

    filename = "Spells_Components.html"

    caption = """Graph of the number of spells that have each attribute listed on the x-axis. The first bar is to show
    the total number of spells so the user can compare the proportion of spells that are affected by each attribute.
    The green bars are components that are required for casting the spell. Verbal means that the spell requires the
    caster to speak some incantation, somatic means the spell requires the caster to make some motions with their hand,
    wand, or staff, and material means the spell requires some physical components to cast the spell. Each spell can
    have any combination of verbal, somatic, and material components. The concentration bar refers to the number of
    spells that require the caster maintain concentration on the spell for its effects to persist; once the caster loses
    concentration, the spell ends. The ritual bar refers to the number of spells that can be cast without consuming a
    spell slot by spending 10 minutes to cast the spell instead of it being instantaneous."""

    if to_png:
        export_png(p, filename=f"{filename.split('.')[0]}.png")
    else:
        save_html(filename, file_html(p, template=HTML_TEMPLATE, resources="cdn", title=p.title.text,
                                      template_variables={"caption": caption, "css_styles": CSS_STYLES}))


def visualize_monster_alignment(to_png=False):
    to_skip = ["any alignment", "unaligned", "any non-good alignment", "any non-lawful alignment",
               "any chaotic alignment", "any evil alignment"]
    ethics_values = ["Chaotic", "Neutral", "Lawful"]
    morals_values = ["Evil", "Neutral", "Good"]
    types_values = ['plant', 'dragon', 'fiend', 'construct', 'giant', 'monstrosity', 'beast', 'undead', 'elemental',
                    'fey', 'aberration', 'celestial', 'humanoid']
    types_colors = ['#2ca02c', '#ff7f0e', '#d62728', '#7f7f7f', '#8c564b', '#ff9896', '#c49c94', '#bcbd22', '#1f77b4',
                    '#98df8a', '#9467bd', '#17becf', '#e377c2']
    totals = {"Chaotic Evil": 0, "Chaotic Neutral": 0, "Chaotic Good": 0, "Neutral Evil": 0, "Neutral Neutral": 0,
              "Neutral Good": 0, "Lawful Evil": 0, "Lawful Neutral": 0, "Lawful Good": 0}
    ethics = []
    morals = []
    names = []
    types_ = []
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
        challenge_rating.append((monster_data["challenge_rating"]))
        types_.append(monster_data["type"])

    for k, v in totals.items():
        ethics_totals.append(k.split()[0])
        morals_totals.append(k.split()[1])
        count_totals.append(v)

    challenge_mapper = LinearInterpolator(
        x=[min(challenge_rating), max(challenge_rating)],
        y=[6, 30]
    )

    count_mapper = LinearInterpolator(
        x=[min(count_totals), max(count_totals)],
        y=[10, 150]
    )

    tooltips = [
        ("Name", "@names"),
        ("CR", "@challenge_rating"),
        ("Type", "@types"),
        ("Morals", "@morals"),
        ("Ethics", "@ethics"),
        ("Total", "@count")
    ]
    source = ColumnDataSource(
        data=dict(ethics=ethics, morals=morals, names=names, challenge_rating=challenge_rating, types=types_))
    source_totals = ColumnDataSource(data=dict(ethics=ethics_totals, morals=morals_totals, count=count_totals))

    p = figure(x_range=ethics_values, y_range=morals_values, width=1200, height=800, tooltips=tooltips,
               title="Monster Alignment Totals and Monster Challenge Ratings", output_backend='webgl')

    monster_cr = p.circle(x=jitter('ethics', width=0.3, range=p.x_range),
                          y=jitter('morals', width=0.3, range=p.y_range),
                          source=source, alpha=0.5,
                          color=factor_cmap('types', palette=types_colors, factors=types_values),
                          size={'field': 'challenge_rating', 'transform': challenge_mapper}, legend_group='types'
                          )
    monster_count = p.square(x='ethics', y='morals', source=source_totals, alpha=0.2, color="red",
                             size={'field': 'count', 'transform': count_mapper},
                             legend_label="Monster Alignment Count")

    toggle_cr = Toggle(label='Monster Challenge Rating', button_type='success', active=True)
    toggle_cr.js_link('active', monster_cr, 'visible')

    toggle_count = Toggle(label='Monster Count', button_type='success', active=True)
    toggle_count.js_link('active', monster_count, 'visible')

    p.toolbar.active_scroll = p.select_one(WheelZoomTool)

    p.legend.click_policy = 'hide'
    p.legend.location = 'top_center'
    p.legend.orientation = 'horizontal'

    filename = "Monsters_Alignment.html"

    caption = """Graph of the distribution of monsters in their respective alignments (x and y position) as well as
    their type (circle color) and challenge rating (circle size). There is also a summary mark (square) that represents
    the total number of monsters that fall into the corresponding alignment (size). The alignment of a monster or
    character is a combination of their ethics (Chaotic, Neutral, Lawful) and their morals (Evil, Neutral, Good). These
    alignments determine the general behavior of the monster and what you can expect from interacting with them. The
    challenge rating of a monster represents the overall difficulty in fighting that monster (i.e the higher the
    challenge rating, the more difficult they are to defeat). The type of the monster is the category that the monster
    falls into. Categories are listed in the legend at the top of the graph."""

    if to_png:
        export_png(p, filename=f"{filename.split('.')[0]}.png")
    else:
        save_html(filename, file_html(p, template=HTML_TEMPLATE, resources="cdn", title=p.title.text,
                                      template_variables={"caption": caption, "css_styles": CSS_STYLES}))


# def visualize_race_stat_bonuses(to_png=False):
#     schools_data = {}
#     spell_list = os.listdir("data/races")
#     for spell_name in spell_list:
#         with open(f"data/spells/{spell_name}", "r") as file:
#             spell_data = json.load(file)
#         spell_school = spell_data["school"]["name"]
#         if spell_school not in schools_data:
#             schools_data[spell_school] = 1
#         else:
#             schools_data[spell_school] += 1
#     schools = []
#     counts = []
#     for k, v in schools_data.items():
#         schools.append(k)
#         counts.append(v)
#     sorted_schools = sorted(schools, key=lambda x: counts[schools.index(x)], reverse=True)
#     p = figure(x_range=sorted_schools, title="Number of Spells by School of Magic", x_axis_label="School of Magic",
#                y_axis_label="Number of Spells", width=750)
#     p.vbar(x=schools, top=counts, legend_label="Number of Spells", width=0.5, bottom=0, color="red")
#     p.xgrid.grid_line_color = None
#
#     output_file("Spells.html")
#
#     show(p)


def visualize_number_of_spells_by_class(to_png=False):
    class_values = ['Sorcerer', 'Wizard', 'Cleric', 'Bard', 'Ranger', 'Warlock', 'Druid', 'Paladin']
    spell_levels = ['cantrip', '1th level', '2th level', '3th level', '4th level', '5th level', '6th level',
                    '7th level', '8th level', '9th level']
    class_data = {'classes': class_values,
                  'cantrip': [0, 0, 0, 0, 0, 0, 0, 0],
                  '1th level': [0, 0, 0, 0, 0, 0, 0, 0],
                  '2th level': [0, 0, 0, 0, 0, 0, 0, 0],
                  '3th level': [0, 0, 0, 0, 0, 0, 0, 0],
                  '4th level': [0, 0, 0, 0, 0, 0, 0, 0],
                  '5th level': [0, 0, 0, 0, 0, 0, 0, 0],
                  '6th level': [0, 0, 0, 0, 0, 0, 0, 0],
                  '7th level': [0, 0, 0, 0, 0, 0, 0, 0],
                  '8th level': [0, 0, 0, 0, 0, 0, 0, 0],
                  '9th level': [0, 0, 0, 0, 0, 0, 0, 0],
                  'total': [0, 0, 0, 0, 0, 0, 0, 0]}
    spell_list = os.listdir("data/spells")
    for spell_name in spell_list:
        with open(f"data/spells/{spell_name}", "r") as file:
            spell_data = json.load(file)
        classes = spell_data["classes"]
        for class_ in classes:
            class_data["cantrip" if not spell_data["level"] else f"{str(spell_data['level'])}th level"][
                class_values.index(class_["name"])] += 1
            class_data["total"][class_values.index(class_["name"])] += 1

    sorted_class_values = sorted(class_values, key=lambda x: class_data["total"][class_values.index(x)], reverse=True)
    p = figure(x_range=sorted_class_values, title="Number of Spells by Class and Spell Level", x_axis_label="Class",
               y_axis_label="Number of Spells", width=750)
    p.vbar_stack(spell_levels, x='classes', legend_label=spell_levels, width=0.5, source=class_data,
                 color=Category10[10], line_width=0)
    p.xgrid.grid_line_color = None

    filename = "Classes_Spells_Levels.html"

    caption = """Graph of the number of spells that each spellcasting class can choose to learn from categorized by the
    level of the spell. Rules for the number of spells each class can learn and if the spells can be swapped out at a
    later time is determined by the ruleset for that class. Any missing categories for a class means that class can't
    learn that level of spell. Cantrips are often thought of as 0th level spells and are spells that are easy to cast
    without much thought and thus do not require a spell slot to cast."""

    if to_png:
        export_png(p, filename=f"{filename.split('.')[0]}.png")
    else:
        save_html(filename, file_html(p, template=HTML_TEMPLATE, resources="cdn", title=p.title.text,
                                      template_variables={"caption": caption, "css_styles": CSS_STYLES}))


if __name__ == '__main__':
    visualize_spells_schools()
    visualize_monster_alignment()
    visualize_spell_components_and_types()
    visualize_number_of_spells_by_class()
