import { Module } from '@nestjs/common';
import { PrismaModule } from './prisma/prisma.module';
import { CatchModule } from './catch/catch.module';


@Module({
  imports: [CatchModule, PrismaModule],
})
export class AppModule {}
