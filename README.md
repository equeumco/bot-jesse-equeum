# Jesse Project Template with Equeum Support

This is template from which you can create your own Jesse project and start using Equeum forecasts.

## Before you start

- [⚡️ Sign Up to the Platform](https://equeum.com/)
- [🎓 Read Platform Documentation](https://equeum.gitbook.io/docs/)
- [💬 Join Our Discord Community](https://discord.gg/J7Dwh3xPVD)

## About Equeum
[Equeum](https://equeum.com/) is a platform founded on the same principles as those of Wall Street quant funds: the fundamental truth being that prices of assets do not move at random, and that by gathering and analyzing vast amounts of data, developers can extract data-based signals for use in building quantitative pricing models. In short, Equeum is all about doing an open, large-scale version of what Wall Street quant firms have been doing for decades.

[Equeum](https://equeum.com/) has, in essence, built a creator economy for quants. Any developer can use the platform for free.  Developers retain ownership, and are fairly compensated for what they create. The models they create are provided to investors to help investors make better, more informed, data-driven investment decisions. These investors pay for this value, and the majority of the revenue generated flows back to developers.

[Equeum](https://equeum.com/) platform features:
- A powerful time-series engine for analyzing and extracting signals from massive and diverse sets of data
- A domain-specific language, EQL, that enables developers – collaboratively, iteratively, and in real-time – to create asset price models
- Seamless integration of on- and off-platform data
- A built-in set of shared tools to facilitate data collection and analysis

## Installation
Assuming that you already [have installed](https://docs.jesse.trade/docs/getting-started) the environment dependencies, you can run the following command to create your project:

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
- [🤖 Jesse Trade strategy](https://github.com/equeumco/bot-jesse-equeum)
- [🤖 Freqtrade strategy](https://github.com/equeumco/bot-freqtrade-equeum)