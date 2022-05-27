-- CreateTable
CREATE TABLE "test_table" (
    "id" INTEGER NOT NULL,
    "name" VARCHAR(55),
    "used_flag" BOOLEAN DEFAULT false,

    CONSTRAINT "test_table_pkey" PRIMARY KEY ("id")
);
