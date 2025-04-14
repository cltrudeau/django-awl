import nox

def common(session):
    session.install("-e", "..")
    session.install("logthing>=1.0.0")
    session.install("screwdriver>=0.15.0")
    session.install("context-temp>=0.11.2")

# 320 is end of life
# 400 is end of life
# 410 is end of life

# 420 is LTS, end of life April 2026; should work with 3.8, but I'm
# deprecating that as the dependencies don't test with it
@nox.session(python=["3.9", "3.10", "3.11", "3.12"])
def test420(session):
    common(session)
    session.install(f"django>=4.2,<4.3")
    session.run("./manage.py", "test", external=True)


# 500 is end of life

# 510, end of life December 2025
@nox.session(python=["3.10", "3.11", "3.12", "3.13"])
def test510(session):
    common(session)
    session.install(f"django>=5.1,<5.2")
    session.run("./manage.py", "test", external=True)


# 520 is LTS, end of life April 2028
@nox.session(python=["3.10", "3.11", "3.12", "3.13"])
def test520(session):
    common(session)
    session.install(f"django>=5.2,<6")
    session.run("./manage.py", "test", external=True)
