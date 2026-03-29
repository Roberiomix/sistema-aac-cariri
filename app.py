.header{background: var(--verde); padding:40px; text-align:center;}
        
        .logo-box{
            /* Este fundo branco suave vai destacar o seu escudo verde */
            background: rgba(255, 255, 255, 0.9); 
            width: 140px; 
            height: 140px; 
            border-radius: 50%; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            margin: 0 auto 20px; 
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            border: 4px solid var(--dourado);
            overflow: hidden;
        }
        
        .logo{
            height: 110px; /* Tamanho ideal para não tocar nas bordas */
            width: auto;
            object-fit: contain;
            /* Filtro para deixar as cores da logo mais vivas contra o fundo */
            filter: drop-shadow(0px 4px 4px rgba(0,0,0,0.2));
        }
