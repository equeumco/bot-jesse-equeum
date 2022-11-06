# Jesse Project Template with Equeum Support

This is template from which you can create your own Jesse project with Equeum support.

## Before you start

- [⚡️ Sign Up to the Platform](https://equeum.com/)
- [🎓 Read Platform Documentation](https://equeum.gitbook.io/docs/)
- [💬 Join Our Discord Community](https://discord.gg/J7Dwh3xPVD)

## Usage
Assuming that you already have installed the environment dependencies, you can run the following command to create your project:

```sh
# you can change "my-project" to any name you want
git clone https://github.com/equeumco/bot-jesse-equeum.git my-project
# to create a .env file of yours
cp .env.example .env
```

Don't forget to update variable `_equeum_token` with right `API Token`, obtained from [Eqeueum Website](https://app.equeum.com/register).

## Running with Docker
While in the project folder run:

```sh
cd docker
docker-compose up
```

That's it! Now open [localhost:9000](http://localhost:9000) in your browser to see the dashboard. 

## Live trading
Please follow [this documentation](https://docs.jesse.trade/docs/livetrade.html#installation) to proceed with live trading.


## Questions?

Join our [Discord community](https://discord.gg/J7Dwh3xPVD) to get fresh news, ask for help and find new strategy ideas.

## Resources

- [⚡️ Website](https://equeum.com/)
- [🎓 Documentation](https://equeum.gitbook.io/docs/)
- [💬 Discord community](https://discord.gg/J7Dwh3xPVD)