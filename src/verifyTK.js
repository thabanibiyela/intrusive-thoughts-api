/*
The following sources were used as a template for the following route.
***************************************************************************************//*

*    Title: MiniFilm-node-auth source code
*    Author: Sotiriadis, S
*    Date: 2022
*    Code version: 2022
*    Availability: https://github.com/steliosot/MiniFilm-node-auth/blob/master/routes/verifyToken.js
*
***************************************************************************************//*
(Version 2022) [Source code]. https://github.com/steliosot/MiniFilm-node-auth/blob/master/routes/verifyToken.js
*/

const jwt = require('jsonwebtoken')
const {send} = require('express/lib/response')

function authentication(req,res,next){
    const authToken = req.header('auth-token')
    if(!authToken){
        return res.status(401).send({message:'Access denied. We could not find your authentication token?'})
    }
    try{
        const verificationSucess = jwt.verify(authToken,process.env.JWT_SECRET)
        req.thinker=verificationSucess
        next()
    }catch(err){
        return res.status(401).send({message:'This authentication token does not work!'})
    }
}

module.exports=authentication