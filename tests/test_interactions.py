import discord
import pytest
import discord.ext.test as dpytest  # noqa: F401


@pytest.mark.asyncio
async def test_message(bot: discord.ext.commands.Bot):

    @bot.tree.command()
    async def my_command(interaction: discord.Interaction):
        await interaction.response.send_message('hola', ephemeral=True)  # noqa
        await interaction.channel.send('hi')

    guild = bot.guilds[0]
    channel = guild.text_channels[0]
    mem = guild.members[0]

    await dpytest.create_interaction('my_command', {}, guild_id=guild.id, channel=channel)
    assert dpytest.verify().message().content('hi')

