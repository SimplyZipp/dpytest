import discord
import pytest
import discord.ext.test as dpytest  # noqa: F401


@pytest.mark.asyncio
async def test_message(bot: discord.ext.commands.Bot):

    @bot.tree.command()
    async def my_command(interaction: discord.Interaction):
        await interaction.response.send_message('hola', ephemeral=True)  # noqa
        await interaction.channel.send('hi')

    @bot.tree.command()
    async def arg_command(interaction: discord.Interaction, msg: str, number: int):
        await interaction.response.send_message(f'{msg}: {number}')  # noqa

    guild = bot.guilds[0]
    channel = guild.text_channels[0]
    mem = guild.members[0]

    iid = await dpytest.create_interaction('my_command', {}, guild_id=guild.id, channel=channel)
    assert dpytest.verify().message().content('hi')
    assert dpytest.verify().interaction(iid).response('hola')
    with pytest.raises(ValueError):
        assert dpytest.verify().interaction(0)

    iid = await dpytest.create_interaction('arg_command', {'msg':'test','number':2}, guild_id=guild.id, channel=channel)
    assert dpytest.verify().interaction(iid).contains().response('test')
    assert dpytest.verify().interaction(iid).contains().response('2')