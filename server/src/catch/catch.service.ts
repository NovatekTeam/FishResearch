import { Injectable } from "@nestjs/common";
import { PrismaService } from "src/prisma/prisma.service";
import * as csv from '@fast-csv/parse'
import { SaveCatchDto } from "./dto/save-catch.dto";
import { plainToInstance } from "class-transformer";
import { validateOrReject } from "class-validator";

@Injectable()
export class CatchService {
    constructor(private prisma: PrismaService){}

    loadCatchRow(dto: SaveCatchDto){
        return this.prisma.fish_catch.create({
            data: dto
        })
    }

    loadCatchRows(dto: SaveCatchDto[]){
        return this.prisma.fish_catch.createMany({
            data: dto
        })
    }

    async loadCsv(file: Express.Multer.File){
        return new Promise((resolve,reject) => {
        const data = []
        csv.parseFile(file.path,{delimiter: ',' , headers: true})
        .on('data', (row) => {
            const catchClass = plainToInstance(SaveCatchDto,row)
            validateOrReject(catchClass).catch( errors => resolve(errors) )
            data.push(row)
        })
        .on('end', () => {      
            resolve(this.loadCatchRows(data))
        }) 
    })     
        
    }


}