# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import requests
import ask_sdk_core.utils as ask_utils

from requests.structures import CaseInsensitiveDict
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name, get_dialog_state, get_slot_value
from ask_sdk_model import Response, DialogState

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)




# This will be launched when the skill is started. The intention is that it gets the user to say their name.

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome, I can build Virtual Machines using Red Hat Ansible, to start with, please tell me your name?."


        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )



#This will record the users name in a session attribute and repeat it back to them.

class mynameisIntentHandler(AbstractRequestHandler):
    """Handler for mynameis Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("mynameis")(handler_input) 
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        name = slots["name"].value
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr['demo_name'] = name
#        session_attr = handler_input.attributes_manager.session_attributes
#        name = get_slot_value("name")
#        session_attr["name"] = name
        speak_output = f"Ok, Hello {name}. Welcome to the Red Hat Ansible Demo. I can build virtual machines. To build one say, build a VM."
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )



# This will make an API call to the AAP server to run the ansible demo.

class build_vmIntentHandler(AbstractRequestHandler):
    """Handler for build_vm Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("build_vm")(handler_input)

    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        name = session_attr['demo_name']

        # type: (HandlerInput) -> Response
        url = "https://xxxxxxxxxxxxxxxx/api/v2/workflow_job_templates/xxxxxxx/launch/"

        PAT_token = "Bearer xxxxxxxxxxxxxxxxxxx"
        headers = CaseInsensitiveDict()
        headers["Authorization"] = PAT_token
        headers["Content-Type"] = "application/json"

        data = '{{ "extra_vars": "name: {0}" }}'.format(name)
        
        resp = requests.post(url, headers=headers, data=data, verify=False)
        code = resp.status_code
        if code == 201:
            speak_output = f"Ok, Red Hat Ansible is a powerful automation tool that can automate almost any device or application in a datacentre. Ansible is building a webserver and creating you a custom website, once finished it will be displayed on the screen in front of you. Until then the screen will provide you with updates on what Ansible is currently doing. Keep an eye on the logos on the floor, as ansible interacts with technology from different vendors, the logos will change. This will only take a few minutes!"
        else:
            speak_output = f"Sorry there was an error. The server returned http error {code}"
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


# intention was to use this to trigger the demo cleanup job. However it make more sense to have that trigger automatically after a wait within ansible. Will still trigger the job, but isnt mentioned to the user - so unlikely anyone will know its there.

class destroy_vmIntentHandler(AbstractRequestHandler):
    """Handler for destroy_vm Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("destroy_vm")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
               
        url = "https://xxxxxxxxxx/api/v2/workflow_job_templates/xxxx/launch/"

        PAT_token = "Bearer xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

        headers = CaseInsensitiveDict()
        headers["Authorization"] = PAT_token
        headers["Content-Type"] = "application/json"
        
        resp = requests.post(url, headers=headers, verify=False)
        code = resp.status_code
        if code == 201:
            speak_output = "Ok, I will destroy the VM. Please wait a few minutes before creating a new one."
        else:
            speak_output = f"Sorry there was an error. The server returned http error {code}"
            
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )



# part of initial helloworld program. Have changed it to ask name in order to trigger the mynameis intent handler

class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello, What is your name?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )




# part of the initial helloworld program. Have changed the help text to get it to ask name to start the demo

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello, to start the demo, please tell me your name?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )



# built in stop intent handler

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


# initially part of helloworld program, have customised it to get it to ask the users name to start the demo

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. If you tell me your name I can start the demo"
        reprompt = "I didn't catch that. What is your name?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response


#built in session end handler

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response



#built in handler

class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


# part of initial built in handlers, customised to ask name to try and trigger the  start of the demo.

class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. To start the demo, please tell me your name"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.



sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(mynameisIntentHandler())
sb.add_request_handler(build_vmIntentHandler())
sb.add_request_handler(destroy_vmIntentHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
