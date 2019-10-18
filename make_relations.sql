BEGIN;
--
-- Create model User
--
CREATE TABLE "users" ("id" serial NOT NULL PRIMARY KEY, "password" varchar(128) NOT NULL, "username" varchar(30) NOT NULL UNIQUE, "first_name" varchar(30) NOT NULL, "last_name" varchar(30) NOT NULL);
COMMIT;

BEGIN;
--
-- Create model Branches
--
CREATE TABLE "branches" ("id" serial NOT NULL PRIMARY KEY, "name" varchar(255) NOT NULL);
--
-- Create model BranchUpdates
--
CREATE TABLE "branch_updates" ("id" serial NOT NULL PRIMARY KEY, "status" boolean NOT NULL, "branch_id" integer NOT NULL, "user_id" integer NOT NULL);
--
-- Add field users to branches
--
ALTER TABLE "branch_updates" ADD CONSTRAINT "branch_updates_branch_id_fk" FOREIGN KEY ("branch_id") REFERENCES "branches" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "branch_updates" ADD CONSTRAINT "branch_updates_user_id_fk" FOREIGN KEY ("user_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "branch_updates_branch_id" ON "branch_updates" ("branch_id");
CREATE INDEX "branch_updates_user_id" ON "branch_updates" ("user_id");
COMMIT;

BEGIN;
--
-- Create model Repositories
--
CREATE TABLE "repositories" ("id" serial NOT NULL PRIMARY KEY, "name" varchar(255) NOT NULL, "stars" integer NOT NULL, pulse_stats jsonb NOT NULL);
CREATE TABLE "repositories_branches" ("id" serial NOT NULL PRIMARY KEY, "repositories_id" integer NOT NULL, "branches_id" integer NOT NULL);
--
-- Create model RepositorySubscriptions
--
CREATE TABLE "repository_subscriptions" ("id" serial NOT NULL PRIMARY KEY, "status" boolean NOT NULL, "repository_id" integer NOT NULL, "user_id" integer NOT NULL);
--
-- Add field users to repositories
--
ALTER TABLE "repositories_branches" ADD CONSTRAINT "repositories_branches_repositories_id_fk" FOREIGN KEY ("repositories_id") REFERENCES "repositories" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "repositories_branches" ADD CONSTRAINT "repositories_branches_branches_id_fk" FOREIGN KEY ("branches_id") REFERENCES "branches" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "repositories_branches" ADD CONSTRAINT "repositories_branches_repositories_id_branches_id_uniq" UNIQUE ("repositories_id", "branches_id");
CREATE INDEX "repositories_branches_repositories_id" ON "repositories_branches" ("repositories_id");
CREATE INDEX "repositories_branches_branches_id" ON "repositories_branches" ("branches_id");
ALTER TABLE "repository_subscriptions" ADD CONSTRAINT "repository_subscriptions_repository_id_fk" FOREIGN KEY ("repository_id") REFERENCES "repositories" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "repository_subscriptions" ADD CONSTRAINT "repository_subscriptions_user_id_fk" FOREIGN KEY ("user_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "repository_subscriptions_repository_id" ON "repository_subscriptions" ("repository_id");
CREATE INDEX "repository_subscriptions_user_id" ON "repository_subscriptions" ("user_id");
COMMIT;

BEGIN;
--
-- Create model Developers
--
CREATE TABLE "developers" ("id" serial NOT NULL PRIMARY KEY, "nickname" varchar(255) NOT NULL, "avatar_url" varchar(200) NOT NULL);
--
-- Create model DeveloperSubscriptions
--
CREATE TABLE "developer_subscriptions" ("id" serial NOT NULL PRIMARY KEY, "status" boolean NOT NULL, "developer_id" integer NOT NULL, "user_id" integer NOT NULL);
--
-- Add field users to developers
--
ALTER TABLE "developer_subscriptions" ADD CONSTRAINT "developer_subscriptions_developer_id_fk" FOREIGN KEY ("developer_id") REFERENCES "developers" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "developer_subscriptions" ADD CONSTRAINT "developer_subscriptions_user_id_fk" FOREIGN KEY ("user_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "developer_subscriptions_developer_id" ON "developer_subscriptions" ("developer_id");
CREATE INDEX "developer_subscriptions_user_id" ON "developer_subscriptions" ("user_id");
COMMIT;


BEGIN;
--
-- Create model Commits
--
CREATE TABLE "commits" ("id" serial NOT NULL PRIMARY KEY, "creation_date" date NOT NULL, "message" varchar(4096) NOT NULL, "changed_files" varchar(4096)[] NOT NULL);
CREATE TABLE "commits_branches" ("id" serial NOT NULL PRIMARY KEY, "commits_id" integer NOT NULL, "branches_id" integer NOT NULL);
CREATE TABLE "commits_developers" ("id" serial NOT NULL PRIMARY KEY, "commits_id" integer NOT NULL, "developers_id" integer NOT NULL);
--
-- Create model CommitUpdates
--
CREATE TABLE "commit_updates" ("id" serial NOT NULL PRIMARY KEY, "status" boolean NOT NULL, "commit_id" integer NOT NULL, "user_id" integer NOT NULL);
--
-- Add field users to commits
--
ALTER TABLE "commits_branches" ADD CONSTRAINT "commits_branches_commits_id_fk" FOREIGN KEY ("commits_id") REFERENCES "commits" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "commits_branches" ADD CONSTRAINT "commits_branches_branches_id_fk" FOREIGN KEY ("branches_id") REFERENCES "branches" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "commits_branches" ADD CONSTRAINT "commits_branches_commits_id_branches_id_uniq" UNIQUE ("commits_id", "branches_id");
CREATE INDEX "commits_branches_commits_id" ON "commits_branches" ("commits_id");
CREATE INDEX "commits_branches_branches_id" ON "commits_branches" ("branches_id");
ALTER TABLE "commits_developers" ADD CONSTRAINT "commits_developers_commits_id_fk" FOREIGN KEY ("commits_id") REFERENCES "commits" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "commits_developers" ADD CONSTRAINT "commits_developers_developers_id_fk" FOREIGN KEY ("developers_id") REFERENCES "developers" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "commits_developers" ADD CONSTRAINT "commits_developers_commits_id_developers_id_uniq" UNIQUE ("commits_id", "developers_id");
CREATE INDEX "commits_developers_commits_id" ON "commits_developers" ("commits_id");
CREATE INDEX "commits_developers_developers_id" ON "commits_developers" ("developers_id");
ALTER TABLE "commit_updates" ADD CONSTRAINT "commit_updates_commit_id_fk" FOREIGN KEY ("commit_id") REFERENCES "commits" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "commit_updates" ADD CONSTRAINT "commit_updates_user_id_fk" FOREIGN KEY ("user_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "commit_updates_commit_id" ON "commit_updates" ("commit_id");
CREATE INDEX "commit_updates_user_id" ON "commit_updates" ("user_id");
COMMIT;

