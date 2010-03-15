from braintree.environment import Environment

class Configuration:
    @staticmethod
    def base_merchant_path():
        return "/merchants/" + Configuration.merchant_id

    @staticmethod
    def server_and_port():
        config = Configuration()
        return config.server() + ":" + str(config.port())

    @staticmethod
    def ssl():
        if Configuration.environment == Environment.DEVELOPMENT:
            return False
        else:
            return True

    def port(self):
        if Configuration.environment == Environment.DEVELOPMENT:
            return 3000
        else:
            return 443

    def server(self):
        if Configuration.environment == Environment.DEVELOPMENT:
            return "localhost"
        elif Configuration.environment == Environment.PRODUCTION:
            return "www.braintreegateway.com"
        elif Configuration.environment == Environment.SANDBOX:
            return "sandbox.braintreegateway.com"
