/*
The following sources were used as a template for the following model.
***************************************************************************************//*

*    Title: MiniFilm-node-auth source code
*    Author: Sotiriadis, S
*    Date: 2022
*    Code version: 2022
*    Availability: https://github.com/steliosot/MiniFilm-node-auth/blob/master/models/User.js
*
***************************************************************************************//*
(Version 2022) [Source code]. https://github.com/steliosot/MiniFilm-node-auth/blob/master/models/User.js

*/


const mongoose = require('mongoose')

const ThinkerSchema = mongoose.Schema({

    //TODO - Constraints and limits
    "username":{
        type:String,
        required:true
    },
    "email":{
        type:String,
        required:true
    },
    "dateJoined":{
        type:Date,
        default:Date.now
    },
    "firstName":{
        type:String,
        required:true
    },
    "lastName":{
        type:String,
        required:true
    },
    "password":{
        type:String,
        required:true
    },
    "echoChambers":{
        type:[String],
        default:["General"]
    },
    "role":{
            type:String,
            default:"user"
        }
})


const thinker_model = mongoose.model('Thinkers',ThinkerSchema)
const test_thinker_model = mongoose.model('_test_thinkers',ThinkerSchema)
module.exports = { ThinkerModel: thinker_model, TestThinkerModel: test_thinker_model }