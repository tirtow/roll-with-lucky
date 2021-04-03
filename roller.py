import discord


class Roller:
    async def start_roll(self, channel):
        """
        Let's start rollin
        """

        # Build the embed, we'll add reactions for users to use to this
        # and add a roll history to it
        self.__embed = discord.Embed(
            title="Use a reaction to roll",
            color=0x269B42)

        # Cool now send the embed on it's way
        msg = await channel.send(embed=self.__embed)

        # Now add the reactions for users
        reactions = [
            "1️⃣",
            "2️⃣",
            "4️⃣",
            "6️⃣",
            "🔟",
            "⏺",    # Twenty cause there's no 20 /shrug
            "❌"    # Clear the history
        ]
        for reaction in reactions:
            await msg.add_reaction(reaction)
