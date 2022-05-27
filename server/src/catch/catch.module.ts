import { Module } from "@nestjs/common";
import { MulterModule } from "@nestjs/platform-express";
import { CatchController } from "./catch.controller";
import { CatchService } from "./catch.service";

@Module({
    imports: [MulterModule.register({
        dest:'./upload'
    })],
    controllers: [CatchController],
    providers: [CatchService]
})
export class CatchModule {}