import discord
import random


class Roller:
    """
    Class to handle rolling
    """

    async def start_roll(self, channel):
        """
        Let's start rollin

        channel - the channel the message was sent in
        """

        random.seed()

        # Setup an empty list to store the line history
        self.__lines = []

        # Send the embed
        self.__msg = await channel.send(embed=self.__get_embed())

        # Now add the reactions for users
        self.__reactions = [
            "1️⃣",
            "2️⃣",
            "4️⃣",
            "6️⃣",
            "🔟",
            "⏺"     # Twenty cause there's no 20 /shrug
        ]
        for reaction in self.__reactions:
            await self.__msg.add_reaction(reaction)

    async def roll(self, payload, user):
        """
        Roll the dice

        payload - the add/remove event payload
        user    - the user that rolled
        """

        if self.__reaction_for_roll(payload):
            # Translate the emoji to faces
            faces = self.__emoji_to_face_count(payload.emoji.name)

            if faces != 0:
                # Do the actual roll
                result = self.__roll_die(faces)

                # Build the line
                line = "**{0}** rolled a {1} for a **{2}**".format(
                    user.name, payload.emoji.name, result)

                # And finally update the message
                await self.__add_description_line(line)

    def __reaction_for_roll(self, payload):
        """
        Check that the reaction was to the current message and that the reaction
        was one of the reactions the bot added

        payload - the reaction event payload

        Returns True if we should handle the reaction, false otherwise
        """

        if (self.__msg.id != payload.message_id):
            return False
        return payload.emoji.name in self.__reactions

    def __emoji_to_face_count(self, emoji):
        """
        Returns the dice face count for the given emoji

        emoji - the emoji name from the reaction

        Returns the face count
        """

        if emoji == "1️⃣":
            return 1
        if emoji == "2️⃣":
            return 2
        if emoji == "4️⃣":
            return 4
        if emoji == "6️⃣":
            return 6
        if emoji == "🔟":
            return 10
        if emoji == "⏺":
            return 20
        return 0

    def __roll_die(self, faces):
        """
        Do the actually die roll

        faces - the number of faces on the die

        Returns the result
        """

        # First handle some special case
        if faces == 0:
            return "Error: unknown emoji"
        if faces == 1:
            return "bruh"

        # Otherwise just do a normal roll
        return random.randint(1, faces)

    async def __add_description_line(self, line):
        """
        Adds a line to the embed

        line - the line to add
        """

        # Only store the last 20 lines so pop the first (oldest) line if at max
        # then add the new line
        if len(self.__lines) == 20:
            self.__lines.pop(0)
        self.__lines.append(line)

        # Now convert the list into a string
        description = ""
        for i in range(0, len(self.__lines)):
            if i > 0:
                description += "\n"
            description += str(i + 1) + ". " + self.__lines[i]

        # Now we need to build a new embed to add
        embed = self.__get_embed(description)
        await self.__msg.edit(embed=embed)

    def __get_embed(self, description=""):
        """
        Gets an empty embed for the message

        description - the description (default "")

        Returns the embed
        """

        return discord.Embed(
            title="Use a reaction to roll",
            color=0x269B42,
            description=description)
