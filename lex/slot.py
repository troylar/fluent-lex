import boto3


class Slot:
    def __init__(self, **kwargs):
        self.name = kwargs.get('Name')
        self.description = kwargs.get('Description')
        self.checksum = kwargs.get('Checksum')
        self.value = kwargs.get('Value')
        self.create_version = kwargs.get('CreateVersion', False)
        self.value_selection_strategy = kwargs.get('ValueSelectionStrategy', 'ORIGINAL_VALUE')
        self.synonyms = kwargs.get('Synonyms')

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

    def apply(self):
        client = boto3.client('lex-models')
        slot_j = { "name": self.name,
                   "enumerationValues": [ { "value": self.value } ],
                   "valueSelectionStrategy": self.value_selection_strategy}
        if self.description:
            slot_j['description'] = self.description
        if self.synonyms:
            slot_j['enumerationValues']['synonyms'] = self.synonyms
        if self.checksum:
            slot_j['checksum'] = self.checksum
        client.put_slot_type(**slot_j)
