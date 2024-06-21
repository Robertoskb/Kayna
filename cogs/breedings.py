import discord
from discord.ext import commands
from db.models import Monster
from channels.db import database_sync_to_async
from django.db.models import Q


@database_sync_to_async
def get_monster_breedings(name, rarety):
    monster = Monster.objects.filter(
        Q(name_translations__portuguese_name__icontains=name) |
        Q(name_translations__english_name__icontains=name), rarety__name=rarety
    ).prefetch_related('name_translations', 'rarety').first()

    if monster:
        prefetch_list = ['monster_1', 'monster_2', 'monster_3', 'island']
        prefetch_list += ['monster_1__name_translations',
                          'monster_2__name_translations',
                          'monster_3__name_translations',
                          'island__name_translations']
        return list(monster.breedings.all().prefetch_related(*prefetch_list))
    return []


def translate_name(monster, language):
    if monster is None:
        return
    translations = {
        'Portuguese': monster.name_translations.portuguese_name,
        'English': monster.name_translations.english_name,
        'Spanish': monster.name_translations.spanish_name,
    }

    return translations[language]


def tranlate_island(island, language):
    if island is None:
        return
    translations = {
        'Portuguese': island.name_translations.portuguese_name,
        'English': island.name_translations.english_name,
        'Spanish': island.name_translations.spanish_name,
    }

    return translations[language]


def get_embed(breedings, language):
    monster_obj = breedings[0].monster
    embed = discord.Embed(url=str(monster_obj.url), title=monster_obj.name)
    embed.set_thumbnail(
        url=monster_obj.image_url,)

    default_times, enhancend_times = set(), set()
    for breed in breedings:
        m1, m2, m3 = breed.monster_1, breed.monster_2, breed.monster_3
        m1_name, m2_name, m3_name = (translate_name(m1, language),
                                     translate_name(m2, language),
                                     translate_name(m3, language))
        if breed.monster_3:
            value = f'Any({m1_name}, {m2_name}, {m3_name})'
        elif m2 is None:
            value = f'{m1_name} + Three elements'
        else:
            value = f'{m1_name} + {m2_name}'

        embed.add_field(
            name=tranlate_island(breed.island, language) or 'any island',
            value=value, inline=False)
        default_times.add(breed.default_time)
        enhancend_times.add(breed.enhanced_time)

    embed.set_footer(
        text=f'Default Time: {"; ".join(map(str, default_times))}\n'
        f'Enhanced: {"; ".join(map(str, enhancend_times))}')

    return embed


class Breedings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name='breeding', description='Get the breeding combinations of a monster')  # noqa:E501
    @discord.option(name='monster', description='The name of the monster')  # noqa:E501
    @discord.option(name='rarety', choices=['Common', 'Rare', 'Epic'], description='The rarety of the monster')  # noqa:E501
    @discord.option(name='language', choices=['Portuguese', 'English', 'Spanish'], description='The language you want to see the results')  # noqa:E501
    async def breeding(self, ctx, monster: str, rarety: str, language: str):
        breedings = await get_monster_breedings(name=monster, rarety=rarety)
        if not breedings:
            return await ctx.respond('Monstro sem combinações ou inexistente', ephemeral=True)

        embed = get_embed(breedings, language)

        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(Breedings(client))
