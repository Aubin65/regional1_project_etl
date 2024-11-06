import luigi
from transform.code.transform import TransformJoueur  # noqa

if __name__ == "__main__":
    luigi.run(["--module", "transform.code.transform", "TransformJoueur", "--local-scheduler"])
