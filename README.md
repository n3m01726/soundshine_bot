# soundshine_bot/soundshine_bot/README.md

# Soundshine Radio Bot

Welcome to the Soundshine Radio Bot project! This bot is designed to provide a seamless experience for listening to the Soundshine Radio stream on Discord. Below you will find setup instructions, usage guidelines, and a brief overview of the bot's features.

## Features

- **Play Stream**: Users can play the Soundshine Radio stream in a voice channel.
- **Join Voice Channel**: The bot can join the user's voice channel.
- **Stop Stream**: Admins can stop the stream and disconnect the bot from the voice channel.
- **Now Playing**: Users can check what song is currently playing on the stream.
- **Stream Stats**: Admins can view the current number of listeners and the bitrate of the stream.
- **Schedule**: Users can view the programming schedule in an interactive format.
- **Random Wallpaper**: Users can retrieve a random photo from Unsplash.
- **Quiz**: Users can participate in a quiz with multiple-choice questions.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/soundshine_bot.git
   cd soundshine_bot
   ```

2. **Install Dependencies**:
   Make sure you have Python 3.8 or higher installed. Then, install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables**:
   Create a `.env` file in the root directory and add the following variables:
   ```
   BOT_TOKEN=your_bot_token
   UNSPLASH_API=your_unsplash_api_key
   ```

4. **Run the Bot**:
   You can start the bot by running:
   ```bash
   python src/bot.py
   ```

## Usage

- Use the command prefix `!s` followed by the command name to interact with the bot. For example:
  - `!s play` to start playing the stream.
  - `!s stop` to stop the stream.
  - `!s np` to see the current song.
  - `!s stats` to view stream statistics (admin only).
  - `!s schedule` to view the programming schedule.
  - `!s getwall` to get a random wallpaper.
  - `!s quiz` to start a quiz.

## Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
