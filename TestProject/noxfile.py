import nox

def common(session):
    session.install("-e", "..")
    session.install("logthing>=1.0.0")
    session.install("screwdriver>=0.15.0")
    session.install("waelstow>=0.11.1")
    session.install("context-temp>=0.11.2")

# 320 is end of life
# 400 is end of life
# 410 is end of life

# 420 is LTS, end of life April 2026
@nox.session(python=["3.8", "3.9", "3.10", "3.11", "3.12"])
def test420(session):
    common(session)
    session.install(f"django>=4.2,<4.3")
    session.run("./manage.py", "test", external=True)


# 500, end of life April 2025
@nox.session(python=["3.10", "3.11", "3.12"])
def test420(session):
    common(session)
    session.install(f"django>=5.0,<5.1")
    session.run("./manage.py", "test", external=True)


# 510, end of life December 2025
@nox.session(python=["3.10", "3.11", "3.12", "3.13"])
def test420(session):
    common(session)
    session.install(f"django>=5.1,<5.2")
    session.run("./manage.py", "test", external=True)
