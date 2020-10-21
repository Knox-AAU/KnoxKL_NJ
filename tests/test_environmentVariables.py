from environment.EnvironmentConstants import EnvironmentVariables as ev

class Test:

    def test_is_singleton(self):
        instance = ev()
        # Check that the address of the objects are the same
        assert instance == ev()
    
    def test_default_value(self):
        instance = ev()
        non_existing_key = "ThisKeyDoesHopeFullyNotExistInAnyDotEnvironment"
        default_value = "This value is default"

        result: str = instance.get_value(non_existing_key, default_value)
        assert result.__eq__(default_value)