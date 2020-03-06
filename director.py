from flask import Flask, jsonify
#from flask_api import status
import json

########## Custom Exceptions ##############

class Error(Exception):
    """Base class for Errors in the Module
    """

class FormatError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

########## ConfigHandler Setup ##############

class ConfigHandler:
    def __init__(self):
        self.interactions = 0
        self.upgrades = 0
        self.rollbacks = 0
        self.resets = 0
        self.default = {}
        self.default.update(self.createDefault())
        self.latest = self.default
        self.previous = {}

    @staticmethod
    def createDefault():
        """
        Add default configuration to config_store
        """
        default_config = {"config":
                            {"version": 0,
                            "tag": "default",
                            "test": "loopback",
                            "platform": "activemq_artemis"
                            }
                        }
        return default_config

    def getDefault(self):
        return self.__getattribute__('default')

    def upgrade(self, config):
        try:
            self.interactions +=1
            self.upgrades += 1
            if not isinstance(config, dict):
                raise TypeError('Argument must be type dict')
            self.previous = self.latest
            self.latest = config
        except TypeError as err:
            print(err)

    def rollback(self):
        try:
            self.interactions +=1
            self.rollbacks += 1
            if len(self.previous) < 1:
                self.previous = self.default
            self.latest = self.previous
        except TypeError as err:
            print(err)

    def reset(self):
        try:
            self.interactions +=1
            self.resets += 1
            self.latest = self.default
        except TypeError as err:
            print(err)

    def getMetrics(self):
        return {'interactions': self.interactions, 'upgrades': self.upgrades, 'rollbacks': self.rollbacks, 'resets': self.resets}

########## Flask Setup ##############

# POST - Used to receive data
# GET - Used to send data to the requestor

app = Flask(__name__)

# GET /config
@app.route('/config', methods=['GET'])
@app.route('/config/<string:name>', methods=['GET'])
def get_config(name='latest'):
    """
    Returns the configuration as a json string
    Default value = 'latest'
    """
    try:
        result = getattr(cfg, name)
        return jsonify(result)
    except NameError:
        print("ConfigHandler was not initialized")
        return jsonify({})
    except AttributeError:
        print("Invalid config name provided")
        return jsonify({})


# GET /metrics
@app.route('/metrics', methods=['GET'])
def fetch_metrics():
    """
    Returns the configuration as a json string
    Default value = 'latest'
    """
    try:
        result = cfg.getMetrics()
        return jsonify(result)
    except NameError:
        print("ConfigHandler was not initialized")
        return jsonify({})

#    preexisting tags: default, latest
# POST /config/update {test_type: preset_test}
# POST /config/reset
# POST /config/rollback

if __name__ == '__main__':
    cfg = ConfigHandler()
    app.run(port=5000)
    # print(cfg.getDefault())
    # print(cfg.default)
    # print(cfg.latest)
    # print(cfg.previous)
    # new_config = {"config":
    #                 {"version": 1,
    #                 "tag": "new",
    #                 "test": "loopback",
    #                 "platform": "activemq_artemis"
    #                 }
    #             }
    # cfg.upgrade(new_config)
    # print(cfg.latest)
    # cfg.rollback()
    # print(cfg.latest)
    # print(get_config())