import boto3


class WithMessage:
    def __init__(self, **kwargs):
        self.key = 'N/A'
        self.group_number = kwargs.get('GroupNumber')
        self.max_attempts = kwargs.get('MaxAttempts')
        self.messages = []

    def _to_message(self, content_type, content, group_number):
        message_j = {'contentType': content_type,
                     'content': content}
        if group_number:
            message_j['groupNumber'] = group_number
        return message_j

    def _to_json(self):
        self.data[self.key]['messages'] = self.messages
        if self.max_attempts:
            self.data[self.key]['maxAttempts'] = self.max_attempts
        if self.group_number:
            self.data[self.key]['groupNumber'] = self.group_number
        return

    def with_message(self, content_type, content, group_number):
        self.messages.append(self._to_message(content_type, content, group_number))
        return self


class DialogHookCode:
    def __init__(self, **kwargs):
        self.uri = kwargs.get('Uri')
        self.messageVersion = kwargs.get('MessageVersion')


class FulfillmentActivity:
    def __init__(self, **kwargs):
        self.type = kwargs.get('Type')
        self.code_hook = kwargs.get('CodeHook')

class ConfirmationPrompt(WithMessage):
    def __init__(self, **kwargs):
        super(ConfirmationPrompt, self).__init__(**kwargs)
        self.key = 'confirmationPrompt'


class RejectionStatement(WithMessage):
    def __init__(self, **kwargs):
        super(RejectionStatement, self).__init__(**kwargs)
        self.key = 'rejectionStatement'
        self.max_attempts = None


class Prompt(WithMessage):
    def __init__(self, **kwargs):
        super(Prompt, self).__init__(**kwargs)
        self.key = 'prompt'


class FollowUpPrompt(WithMessage):
    def __init__(self, **kwargs):
        super(FollowUpPrompt, self).__init__(**kwargs)
        self.key = 'followUpPrompt'


class IntentSlot(WithMessage):
    def __init__(self, **kwargs):
        self.name = kwargs.get('Name')
        self.description = kwargs.get('Description')
        self.slot_constraint = kwargs.get('SlotConstraint')
        self.slot_type = kwargs.get('SlotType')
        self.slot_type_version = kwargs.get('SlotTypeVersion')
        self.value_elicitation_prompt = {"messages": []}
        self.max_attempts = kwargs.get('PromptMaxAttempts', 3)
        self.priority = kwargs.get('Priority')
        self.sample_utterances = kwargs.get('SampleUtterances')
        self.response_card = kwargs.get('ResponseCard')
        super(IntentSlot, self).__init__(**kwargs)

    def with_name(self, name):
        self.name = name
        return self

    def with_description(self, description):
        self.description = description
        return self

    def with_slot_constraint(self, slot_constraint):
        self.slot_constraint = slot_constraint
        return self

    def with_slot_type(self, slot_type):
        self.slot_type = slot_type
        return self

    def with_slot_type_version(self, slot_type_version):
        self.slot_type_version = slot_type_version
        return self

    def with_value_elicitation_prompt(self, value_elicitation_prompt):
        self.value_elicitation_prompt = value_elicitation_prompt
        return self

    def with_priority(self, priority):
        self.priority = priority
        return self

    def with_sample_utterances(self, sample_utterances):
        self.sample_utterances = sample_utterances
        return self

    def with_response_card(self, response_card):
        self.response_card = response_card
        return self

    def with_value_elicitation_prompt_message(self, content_type, content, group_number):
        self.value_elicitation_prompt['messages'].append(
           self._to_message(content_type, content, group_number))
        return self

    def with_prompt_max_attempts(self, max_attempts):
        self.value_elicitation_prompt['maxAttempts'] = max_attempts
        return self

    def with_prompt_response_card(self, response_card):
        self.value_elicitation_prompt['responseCard'] = response_card
        return self


class Intent:
    def __init__(self, **kwargs):
        self.name = kwargs.get('Name')
        self.description = kwargs.get('Description')
        self.checksum = kwargs.get('Checksum')
        self.value = kwargs.get('Value')
        self.create_version = kwargs.get('CreateVersion', False)
        self.value_selection_strategy = kwargs.get('ValueSelectionStrategy', 'ORIGINAL_VALUE')
        self.synonyms = kwargs.get('Synonyms')
        self.confirmation_prompt = kwargs.get('ConfirmationPrompt', {})
        self.rejection_statement = kwargs.get('RejectionStatement', {})
        self.follow_up_prompt = kwargs.get('FollowUpPrompt', {})
        self.parentIntentSignature = kwargs.get('ParentIntentSignature')
        self.checksum = kwargs.get('Checksum')
        self.create_version = kwargs.get('CreateVersion', False)

    def with_name(self, name):
        self.name = name
        return self

    def with_description(self, description):
        self.description = description
        return self

    def with_checksum(self, checksum):
        self.checksum = checksum
        return self

    def with_value(self, value):
        self.value = value
        return self

    def with_synonyms(self, synonyms):
        self.synonyms = synonyms
        return self

    def with_create_version(self, create_version):
        self.create_version = create_version
        return self

    def with_value_selection_strategy(self, strategy):
        self.value_selection_strategy = strategy
        return self

    def with_confirmation_prompt(self, confirmation_prompt):
        self.confirmation_prompt = confirmation_prompt
        return self

    def with_rejection_statement(self, rejection_statement):
        self.rejection_statement = rejection_statement
        return self

    def with_follow_up_prompt(self, follow_up_prompt):
        self.follow_up_prompt = follow_up_prompt
        return self

    def with_conclusion_statement(self, conclusion_statement):
        self.conclusion_statement = conclusion_statement
        return self

    def with_dialog_hook(self, dialog_hook):
        self.dialog_hook = dialog_hook
        return self


    def apply(self):
        client = boto3.client('lex-models')
        slot_j = {"name": self.name,
                  "enumerationValues": [{"value": self.value}],
                  "valueSelectionStrategy": self.value_selection_strategy}
        if self.description:
            slot_j['description'] = self.description
        if self.synonyms:
            slot_j['enumerationValues']['synonyms'] = self.synonyms
        if self.checksum:
            slot_j['checksum'] = self.checksum
        client.put_slot_type(**slot_j)
