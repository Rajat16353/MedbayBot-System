import { Disease } from "./disease.model";

export class MessageModel{
    mode:string;
    response:string[];
    found_symptoms:string[];
    disease_list:Disease[];
    co_occuring:any[];
    predict:number;
}