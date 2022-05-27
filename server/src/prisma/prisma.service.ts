import { Injectable, INestApplication } from "@nestjs/common";
import  { PrismaClient }  from "@prisma/client";

@Injectable()
export class PrismaService extends PrismaClient {
  constructor() {
      super({
          datasources: {
              db: {
                  url: 'postgresql://postgres:super_secret@allin-srv:5432/postgres?schema=hakaton'
              }
          }
      })
  }

  async enableShutdownHooks(app: INestApplication) {
    this.$on('beforeExit', async () => {
      await app.close();
    });
  }
    
}