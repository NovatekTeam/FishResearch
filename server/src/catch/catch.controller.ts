import { Body, Controller, Post, UploadedFile, UseInterceptors } from "@nestjs/common";
import { FileInterceptor } from "@nestjs/platform-express";
import { CatchService } from "./catch.service";
import { SaveCatchDto } from "./dto/save-catch.dto";


@Controller('catch')
export class CatchController {    
    constructor(private catchService : CatchService){}

    @Post('loadcsv')
    @UseInterceptors(FileInterceptor('file'))
    loadcsv(@UploadedFile() file: Express.Multer.File){        
        this.catchService.loadCsv(file)
    }

    @Post('loadone')
    loadCatchOne(@Body() dto: SaveCatchDto){
        return this.catchService.loadCatchDictRow(dto)
    }

    @Post('loadmany')
    loadCatchMany(@Body() dto: SaveCatchDto[]){
        return this.catchService.loadCatchDictRows(dto)
    }

}