from src.mastermind import Mastermind, MastermindDuplicate


class TestMastermind:
    def test_create_default_game(self):
        game = Mastermind()

        assert game.num_pegs == 4
        assert game.num_colors == 6
        assert len(game.secret_code) == 4

    def test_check_code(self, mocker):
        generate_code_mock = mocker.patch.object(Mastermind, "generate_secret_code")
        generate_code_mock.return_value = "ABCD"
        game = Mastermind()

        assert game.check_code("EEEE") == (0, 0)
        assert game.check_code("AAAA") == (1, 0)
        assert game.check_code("CCAA") == (0, 2)
        assert game.check_code("DCBA") == (0, 4)
        assert game.check_code("ABDC") == (2, 2)
        assert game.check_code("ABCD") == (4, 0)

        assert game.secret_code == "ABCD"
        game.generate_secret_code.assert_called_once_with()


class TestMastermindDuplicate:
    def test_create_default_game(self):
        game = MastermindDuplicate()

        assert game.num_pegs == 4
        assert game.num_colors == 6
        assert len(game.secret_code) == 4

    def test_check_code(self, mocker):
        generate_code_mock = mocker.patch.object(MastermindDuplicate, "generate_secret_code")
        generate_code_mock.return_value = "AACD"
        game = MastermindDuplicate()

        assert game.check_code("EEEE") == (0, 0)
        assert game.check_code("AAAA") == (2, 0)
        assert game.check_code("CCAA") == (0, 3)
        assert game.check_code("DCBA") == (0, 3)
        assert game.check_code("ABDC") == (1, 2)
        assert game.check_code("ABCD") == (3, 0)
        assert game.check_code("AACD") == (4, 0)

        assert game.secret_code == "AACD"
        game.generate_secret_code.assert_called_once_with()
