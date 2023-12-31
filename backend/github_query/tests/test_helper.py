import github_query.util.helper as helper


class TestHelper:
    def test_generate_file_name(self):
        file_name = helper.generate_file_name()
        assert len(file_name) == 6

    def test_add_a_year(self):
        time = "1995-11-11T00:00:00Z"
        assert "1996-11-11T00:00:00Z" == helper.add_a_year(time)

    def test_in_time_period(self):
        mid = "2021-06-01T00:00:00Z"
        start = "2021-01-01T00:00:00Z"
        end = "2022-01-01T00:00:00Z"
        assert helper.in_time_period(mid, start, end)
