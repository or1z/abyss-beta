# Abyss [BETA]

Abyss [BETA] is a self-bot for Discord featuring profile management, message reaction automation, message sniping, and more. It leverages the Discord API and incorporates encryption for secure profile data storage.

## Features

- **Profile Management**: Save and load multiple profiles with unique tokens and prefixes.
- **Message Reactions**: Automatically react to your messages with a specified emoji.
- **Message Sniping**: Retrieve the last deleted message in a channel.
- **Message Purging**: Delete a specified number of your messages in a channel.
- **Streaming Status**: Set your Discord status to streaming with a custom message.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/or1z/abyss-beta.git
   cd abyss-beta
   ```

2. **Install Dependencies**:
   ```bash
   pip install discord cryptography asyncio
   ```

3. **Run the Bot**:
   ```bash
   python abyss.py
   ```

## Usage

1. Upon running the self-bot, you'll be prompted to load an existing profile or create a new one.
2. Follow the on-screen instructions to manage your profiles and use bot commands.

## Commands

- `react [emoji]`: Set the bot to react to your messages with the specified emoji.
- `snipe`: Retrieve the last deleted message in the current channel.
- `purge [amount]`: Delete a specified number of your messages in the current channel.
- `stream [name]`: Set your status to streaming with the specified name.

## Security

- Profile data is securely stored using encryption (via the `cryptography` library).
- Ensure that your Discord token is kept private and secure.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
