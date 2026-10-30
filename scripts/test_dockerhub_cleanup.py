import subprocess
import tempfile
import unittest

from dockerhub_cleanup import protected_revisions, tags_to_delete


def tag(name, last_updated):
    return {"name": name, "last_updated": last_updated}


class TagsToDeleteTest(unittest.TestCase):
    def test_keeps_the_newest_tags_regardless_of_input_order(self):
        tags = [tag("old", "2026-01-01"), tag("newest", "2026-03-01"), tag("mid", "2026-02-01")]
        self.assertEqual(tags_to_delete(tags, 2, set()), ["old"])

    def test_deletes_nothing_when_fewer_tags_than_keep(self):
        tags = [tag("a", "2026-01-01"), tag("b", "2026-01-02")]
        self.assertEqual(tags_to_delete(tags, 10, set()), [])

    def test_never_deletes_protected_tags(self):
        tags = [
            tag("latest", "2026-01-01"),
            tag("abc1234", "2026-01-02"),
            tag("def5678", "2026-01-03"),
            tag("newest", "2026-01-04"),
        ]
        self.assertEqual(tags_to_delete(tags, 1, {"latest", "abc1234"}), ["def5678"])


class ProtectedRevisionsTest(unittest.TestCase):
    BACKEND = "andy.grails.backend"
    FRONTEND = "andy.grails.frontend"

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = self.tmp.name
        self.git("init", "-q", "-b", "master")

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args):
        subprocess.run(
            ["git", "-c", "user.name=test", "-c", "user.email=test@example.com",
             "-c", "commit.gpgsign=false", *args],
            cwd=self.repo, check=True, capture_output=True,
        )

    def commit(self, **submodules):
        """Commit the given submodule paths pointing at the given 40-char revisions."""
        for path, sha in submodules.items():
            self.git("update-index", "--add", "--cacheinfo", f"160000,{sha},{path}")
        self.git("commit", "-q", "--allow-empty", "-m", "update submodules")

    def test_collects_revisions_of_each_submodule_in_recent_history(self):
        self.commit(**{self.BACKEND: "a" * 40, self.FRONTEND: "1" * 40})
        self.commit(**{self.FRONTEND: "2" * 40})
        self.commit(**{self.FRONTEND: "3" * 40})

        revisions = protected_revisions([self.BACKEND, self.FRONTEND], history=10, cwd=self.repo)

        self.assertEqual(revisions[self.BACKEND], {"aaaaaaa"})
        self.assertEqual(revisions[self.FRONTEND], {"1111111", "2222222", "3333333"})

    def test_only_looks_at_the_requested_number_of_commits(self):
        self.commit(**{self.FRONTEND: "1" * 40})
        self.commit(**{self.FRONTEND: "2" * 40})
        self.commit(**{self.FRONTEND: "3" * 40})

        revisions = protected_revisions([self.FRONTEND], history=2, cwd=self.repo)

        self.assertEqual(revisions[self.FRONTEND], {"2222222", "3333333"})

    def test_tolerates_commits_without_the_submodule(self):
        self.commit()  # no submodules at all yet
        self.commit(**{self.FRONTEND: "1" * 40})

        revisions = protected_revisions([self.BACKEND, self.FRONTEND], history=10, cwd=self.repo)

        self.assertEqual(revisions[self.BACKEND], set())
        self.assertEqual(revisions[self.FRONTEND], {"1111111"})


if __name__ == "__main__":
    unittest.main()
