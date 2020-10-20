import app


class Test:
    parser = app.create_parser()

    def test_expected_default(self):
        expected = "Namespace(debug=False, model='sm', verbose=0)"
        parsed = app.parse_args([], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_verbose_short1(self):
        expected = "Namespace(debug=False, model='sm', verbose=1)"
        parsed = app.parse_args(['-v'], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_verbose_short2(self):
        expected = "Namespace(debug=False, model='sm', verbose=2)"
        parsed = app.parse_args(['-vv'], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_verbose_short3(self):
        expected = "Namespace(debug=False, model='sm', verbose=3)"
        parsed = app.parse_args(['-vvv'], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_verbose_short4(self):
        expected = "Namespace(debug=False, model='sm', verbose=4)"
        parsed = app.parse_args(['-vvvv'], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_verbose_long(self):
        expected = "Namespace(debug=False, model='sm', verbose=1)"
        parsed = app.parse_args(['--verbose'], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_debug_short(self):
        expected = "Namespace(debug=True, model='sm', verbose=0)"
        parsed = app.parse_args(['-l'], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_debug_long(self):
        expected = "Namespace(debug=True, model='sm', verbose=0)"
        parsed = app.parse_args(['--debug'], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_model_short1(self):
        expected = "Namespace(debug=False, model='sm', verbose=0)"
        parsed = app.parse_args(['-m'], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_model_short2(self):
        expected = "Namespace(debug=False, model='sm', verbose=0)"
        parsed = app.parse_args(['-m', 'sm'], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_model_short3(self):
        expected = "Namespace(debug=False, model='md', verbose=0)"
        parsed = app.parse_args(['-m', 'md'], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_model_short4(self):
        expected = "Namespace(debug=False, model='lg', verbose=0)"
        parsed = app.parse_args(['-m', 'lg'], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_model_long1(self):
        expected = "Namespace(debug=False, model='sm', verbose=0)"
        parsed = app.parse_args(['--model'], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_model_long2(self):
        expected = "Namespace(debug=False, model='sm', verbose=0)"
        parsed = app.parse_args(['--model', 'sm'], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_model_long3(self):
        expected = "Namespace(debug=False, model='md', verbose=0)"
        parsed = app.parse_args(['--model', 'md'], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_model_long4(self):
        expected = "Namespace(debug=False, model='lg', verbose=0)"
        parsed = app.parse_args(['--model', 'lg'], parser=self.parser)
        assert str(parsed) == expected

    def test_expected_three_arguments(self):
        expected = "Namespace(debug=True, model='md', verbose=1)"
        parsed = app.parse_args(['-v', '-l', '-m', 'md'], parser=self.parser)
        assert str(parsed) == expected
