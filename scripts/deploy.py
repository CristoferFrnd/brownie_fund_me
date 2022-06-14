from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    # pass the price feed adrress to the constructor
    account = get_account()
    # if we are on a persistant network like rinkeby, use the associated address
    # otherwise use mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        print("network: ", [network.show_active()])
        priceFeedAddress = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        priceFeedAddress = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        priceFeedAddress,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
