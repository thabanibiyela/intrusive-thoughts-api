/*
The following sources were used as a template for the following model.
***************************************************************************************//*

*    Title: MiniFilm-node-auth source code
*    Author: Sotiriadis, S
*    Date: 2022
*    Code version: 2022
*    Availability: https://github.com/steliosot/MiniFilm-node-auth/tree/master
*
***************************************************************************************//*
(Version 2022) [Source code]. https://github.com/steliosot/MiniFilm-node-auth/tree/master

*/


const mongoose = require('mongoose')
const CommentSchema = mongoose.Schema({
    "thinker":{
        type:String
    }
    ,
    "detail":{
        type:String
    },
    "timestamp":{
        type:Date,
        default:Date.now
    }
    })

const comment_model = mongoose.model('Comments',CommentSchema)
const test_comment_model = mongoose.model('_test_comments',CommentSchema)
module.exports = { CommentModel: comment_model, TestCommentModel: test_comment_model }