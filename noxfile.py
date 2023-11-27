import nox

def common(session):
    session.install("logthing>=1.0.0")
    session.install("screwdriver>=0.14.0")
    session.install("waelstow>=0.11.0")
    session.install("context-temp>=0.11.1")


# 320 is LTS until April 2024
@nox.session(python=["3.8", "3.9"])
def test320(session):
    common(session)
    session.install("django>=3.2,<4.0")
    session.run("./load_tests.py", external=True)


# 400 is end of life


# 410 is end of life December 2023
@nox.session(python=["3.8", "3.9", "3.10", "3.11", "3.12"])
def test410(session):
    common(session)
    session.install("django>=4.1,<4.2")
    session.run("./load_tests.py", external=True)


# 420 is LTS, end of life April 2026
@nox.session(python=["3.8", "3.9", "3.10", "3.11", "3.12"])
def test420(session):
    common(session)
    session.install("django>=4.2,<4.3")
    session.run("./load_tests.py", external=True)


# 500 can't be tested due to the need for the --pre flag, run tests manually
