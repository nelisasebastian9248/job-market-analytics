from config.settings import load_settings


def main() -> None:
    settings = load_settings()
    print("Job Market Analytics")
    print(f"Adzuna country: {settings.adzuna_country}")
    print(f"GitHub repos tracked: {len(settings.github_repositories)}")
    print(f"Snowflake database: {settings.snowflake_database or 'not set'}")


if __name__ == "__main__":
    main()
