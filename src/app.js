/*
The following sources were used as a template for the following route.
***************************************************************************************//*

*    Title: MiniFilm-node-auth source code
*    Author: Sotiriadis, S
*    Date: 2022
*    Code version: 2022
*    Availability: https://github.com/steliosot/MiniFilm-node-auth/blob/master/app.js
*
***************************************************************************************//*
(Version 2022) [Source code]. https://github.com/steliosot/MiniFilm-node-auth/blob/master/app.js
*/

const express = require('express')
const app = express()
const mongoose = require('mongoose')
const bodyParser = require('body-parser')
app.use(bodyParser.json())
require('dotenv/config')

//const verifyTK = require('./verifyTK')
const thinkerRoute = require('./routes/thinkers')
const thoughtRoute = require('./routes/thoughts')
const authenticationRoute = require('./routes/authentication')

app.use('/thinkers', thinkerRoute)
app.use('/thoughts', thoughtRoute)
app.use('/signin', authenticationRoute)
app.use('/register', thinkerRoute)


const MURL = process.env.DB_CONNECTOR


app.get('/', (req,res)=>{
    res.send({message:'Welcome to the Homepage!'})
})

try{
    mongoose.connect(MURL)
    console.log({message:'Your mongoDB connector is on...'})
} catch(err) {
    console.log(err)
}
app.listen(3000, ()=>{
    console.log({message:'Your server is up and running...'})
})