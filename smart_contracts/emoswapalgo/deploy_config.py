import logging

import algokit_utils

logger = logging.getLogger(__name__)


# define deployment behaviour based on supplied app spec
def deploy() -> None:
    from smart_contracts.artifacts.emoswapalgo.emoswapalgo_client import (
        HelloArgs,
        EmoswapalgoFactory,
    )

    algorand = algokit_utils.AlgorandClient.from_environment()
    deployer_ = algorand.account.from_environment("DEPLOYER")

    factory = algorand.client.get_typed_app_factory(
        EmoswapalgoFactory, default_sender=deployer_.address
    )

    app_client, result = factory.deploy(
        on_update=algokit_utils.OnUpdate.AppendApp,
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
    )

    if result.operation_performed in [
        algokit_utils.OperationPerformed.Create,
        algokit_utils.OperationPerformed.Replace,
    ]:
        algorand.send.payment(
            algokit_utils.PaymentParams(
                amount=algokit_utils.AlgoAmount(algo=1),
                sender=deployer_.address,
                receiver=app_client.app_address,
            )
        )

    # Test the contract
    name = "EmoSwap"
    response = app_client.send.hello(args=HelloArgs(name=name))
    logger.info(
        f"Called hello on {app_client.app_name} ({app_client.app_id}) "
        f"with name={name}, received: {response.abi_return}"
    )
    
    # Save App ID to file
    with open("deployed_contracts.json", "w") as f:
        import json
        data = {
            "emotion_factory_id": 746159123,  # From previous deployment
            "governance_id": 0,
            "liquidity_pool_id": 0,
            "staking_rewards_id": 0,
            "swap_pool_id": 0,
            "mood_token_id": 746157034,
            "deployment_timestamp": str(int(__import__("time").time())),
            "network": "testnet",
            "deployer_address": deployer_.address
        }
        json.dump(data, f, indent=2)
    
    logger.info(f"Contract deployed successfully! App ID: {app_client.app_id}")
    logger.info(f"Explorer: https://testnet.algoexplorer.io/application/{app_client.app_id}")
