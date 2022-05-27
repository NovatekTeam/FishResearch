import { Body, Controller, ParseArrayPipe, Post, UploadedFile, UseInterceptors } from "@nestjs/common";
import { FileInterceptor } from "@nestjs/platform-express";
import { CatchService } from "./catch.service";
import { SaveCatchDto } from "./dto/save-catch.dto";


@Controller('catch')
export class CatchController {    
    constructor(private catchService : CatchService){}

    @Post('loadcsv')
    @UseInterceptors(FileInterceptor('file'))
    async loadcsv(@UploadedFile() file: Express.Multer.File){        
        const result = await this.catchService.loadCsv(file)
        return result
    }

    @Post('loadone')
    loadCatchOne(@Body() dto: SaveCatchDto){
        return this.catchService.loadCatchRow(dto)
    }

    @Post('loadmany')
    loadCatchMany(@Body(new ParseArrayPipe({ items: SaveCatchDto })) dto: SaveCatchDto[]){
        return this.catchService.loadCatchRows(dto)
    }

}