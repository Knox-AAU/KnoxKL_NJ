from app import create_parser, parse_args


class Test:
    parser = create_parser()

    def test_expected_default(self):
        expected = "Namespace(debug=False, model='sm', verb='info')"
        parsed = parse_args([], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_verb_short1(self):
        expected = "Namespace(debug=False, model='sm', verb='info')"
        parsed = parse_args(['-v', 'info'], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_verb_short2(self):
        expected = "Namespace(debug=False, model='sm', verb='warning')"
        parsed = parse_args(['-v', 'warning'], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_verb_short3(self):
        expected = "Namespace(debug=False, model='sm', verb='error')"
        parsed = parse_args(['-v', 'error'], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_verb_long(self):
        expected = "Namespace(debug=False, model='sm', verb='info')"
        parsed = parse_args(['--verb', 'info'], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_debug_short(self):
        expected = "Namespace(debug=True, model='sm', verb='info')"
        parsed = parse_args(['-l'], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_debug_long(self):
        expected = "Namespace(debug=True, model='sm', verb='info')"
        parsed = parse_args(['--debug'], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_model_short1(self):
        expected = "Namespace(debug=False, model='sm', verb='info')"
        parsed = parse_args(['-m'], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_model_short2(self):
        expected = "Namespace(debug=False, model='sm', verb='info')"
        parsed = parse_args(['-m', 'sm'], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_model_short3(self):
        expected = "Namespace(debug=False, model='md', verb='info')"
        parsed = parse_args(['-m', 'md'], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_model_short4(self):
        expected = "Namespace(debug=False, model='lg', verb='info')"
        parsed = parse_args(['-m', 'lg'], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_model_long1(self):
        expected = "Namespace(debug=False, model='sm', verb='info')"
        parsed = parse_args(['--model'], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_model_long2(self):
        expected = "Namespace(debug=False, model='sm', verb='info')"
        parsed = parse_args(['--model', 'sm'], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_model_long3(self):
        expected = "Namespace(debug=False, model='md', verb='info')"
        parsed = parse_args(['--model', 'md'], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_model_long4(self):
        expected = "Namespace(debug=False, model='lg', verb='info')"
        parsed = parse_args(['--model', 'lg'], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_three_arguments(self):
        expected = "Namespace(debug=True, model='md', verb='info')"
        parsed = parse_args(['-v', 'info', '-l', '-m', 'md'], parser=self.parser)
        assert str(parsed) == expected
